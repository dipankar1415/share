#!/usr/bin/env python3
"""
dipTech Proprietary and Confidential
Optimized Sales KPI Dashboard (Panel + Bokeh)
Run with: panel serve sales_dashboard.py --show --autoreload
"""

import pandas as pd
import panel as pn

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Legend, NumeralTickFormatter
from bokeh.transform import dodge
from bokeh.palettes import Category20
from math import pi

pn.extension("tabulator")

# ---------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------


def load_data():
    df = pd.read_csv("sales_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["year_month"] = df["date"].dt.to_period("M").astype(str)
    return df


df = load_data()

# ---------------------------------------------------------------------
# Widgets
# ---------------------------------------------------------------------

year_select = pn.widgets.MultiChoice(
    name="Years",
    value=sorted(df.year.unique().tolist()),
    options=sorted(df.year.unique().tolist()),
)

region_select = pn.widgets.MultiChoice(
    name="Regions",
    value=sorted(df.region.unique().tolist()),
    options=sorted(df.region.unique().tolist()),
)

product_select = pn.widgets.MultiChoice(
    name="Products",
    value=sorted(df["product"].unique().tolist()),
    options=sorted(df["product"].unique().tolist()),
)

metric_select = pn.widgets.Select(
    name="Primary Metric",
    value="revenue",
    options=["revenue", "profit", "units_sold", "profit_margin"],
)

# ---------------------------------------------------------------------
# Filter pipeline (key optimization)
# ---------------------------------------------------------------------


def filtered_df():
    """Helper to apply current widget filters."""
    dff = df
    if year_select.value:
        dff = dff[dff.year.isin(year_select.value)]
    if region_select.value:
        dff = dff[dff.region.isin(region_select.value)]
    if product_select.value:
        dff = dff[dff["product"].isin(product_select.value)]
    return dff


# ---------------------------------------------------------------------
# KPI summary
# ---------------------------------------------------------------------


@pn.depends(
    year_select.param.value,
    region_select.param.value,
    product_select.param.value,
)
def kpi_summary(_years, _regions, _products):
    dff = filtered_df()
    if dff.empty:
        return pn.pane.Markdown("### No data for selection")

    html = f"""
    <div style="display:flex;gap:24px;justify-content:space-between;
                background:#1565c0;color:white;padding:20px;border-radius:14px;">
        <div><h2>${dff.revenue.sum():,.0f}</h2><p>Total Revenue</p></div>
        <div><h2>${dff.profit.sum():,.0f}</h2><p>Total Profit</p></div>
        <div><h2>{dff.units_sold.sum():,}</h2><p>Units Sold</p></div>
        <div><h2>{dff.profit_margin.mean():.1f}%</h2><p>Avg Margin</p></div>
    </div>
    """
    return pn.pane.HTML(html)


# ---------------------------------------------------------------------
# Trend chart
# ---------------------------------------------------------------------


@pn.depends(
    year_select.param.value,
    region_select.param.value,
    product_select.param.value,
    metric_select.param.value,
)
def trend_chart(_years, _regions, _products, metric):
    dff = filtered_df()
    if dff.empty:
        return pn.pane.Markdown("No data")

    data = dff.groupby("year_month")[metric].sum().reset_index()

    src = ColumnDataSource(data)

    p = figure(
        title=f"{metric.title()} Trend",
        x_range=data.year_month.tolist(),
        height=350,
        sizing_mode="stretch_width",
    )

    p.line("year_month", metric, source=src, line_width=3)
    p.scatter("year_month", metric, source=src, size=6)

    p.add_tools(
        HoverTool(tooltips=[("Month", "@year_month"), (metric, f"@{metric}{{0,0}}")])
    )

    p.xaxis.major_label_orientation = pi / 4

    if metric in ["revenue", "profit"]:
        p.yaxis.formatter = NumeralTickFormatter(format="$0,0")

    return p


# ---------------------------------------------------------------------
# Bar chart helpers
# ---------------------------------------------------------------------


def bar_chart(data, x, y, title, color):
    src = ColumnDataSource(data)
    p = figure(
        x_range=data[x].tolist(), height=300, title=title, sizing_mode="stretch_width"
    )
    p.vbar(x=x, top=y, source=src, width=0.7, color=color)
    p.add_tools(HoverTool(tooltips=[(x, f"@{x}"), (y, f"@{y}{{0,0}}")]))
    p.xaxis.major_label_orientation = pi / 4
    p.yaxis.formatter = NumeralTickFormatter(format="$0,0")
    return p


# ---------------------------------------------------------------------
# Regional / product / sales rep
# ---------------------------------------------------------------------


@pn.depends(
    year_select.param.value,
    region_select.param.value,
    product_select.param.value,
)
def region_chart(_years, _regions, _products):
    dff = filtered_df()
    if dff.empty:
        return pn.pane.Markdown("No data")
    data = dff.groupby("region").revenue.sum().reset_index()
    return bar_chart(data, "region", "revenue", "Revenue by Region", "#28a745")


@pn.depends(
    year_select.param.value,
    region_select.param.value,
    product_select.param.value,
)
def product_chart(_years, _regions, _products):
    dff = filtered_df()
    if dff.empty:
        return pn.pane.Markdown("No data")
    data = dff.groupby("product").revenue.sum().reset_index()
    return bar_chart(data, "product", "revenue", "Revenue by Product", "#dc3545")


@pn.depends(
    year_select.param.value,
    region_select.param.value,
    product_select.param.value,
)
def sales_rep_chart(_years, _regions, _products):
    dff = filtered_df()
    if dff.empty:
        return pn.pane.Markdown("No data")
    data = dff.groupby("sales_rep").revenue.sum().nlargest(10).reset_index()
    return bar_chart(data, "sales_rep", "revenue", "Top 10 Sales Reps", "#ffc107")


# ---------------------------------------------------------------------
# YoY chart
# ---------------------------------------------------------------------


@pn.depends(
    year_select.param.value,
    region_select.param.value,
    product_select.param.value,
)
def yoy_chart(_years, _regions, _products):
    dff = filtered_df()
    if dff.empty:
        return pn.pane.Markdown("No data")

    data = dff.groupby("year")[["revenue", "profit"]].sum().reset_index()
    data["year_str"] = data["year"].astype(str)
    src = ColumnDataSource(data)

    p = figure(
        x_range=data["year_str"].tolist(),
        height=350,
        title="Year-over-Year Performance",
    )

    r1 = p.vbar(
        x=dodge("year_str", -0.2, range=p.x_range),
        top="revenue",
        source=src,
        width=0.35,
        color="#2596be",
    )
    r2 = p.vbar(
        x=dodge("year_str", 0.2, range=p.x_range),
        top="profit",
        source=src,
        width=0.35,
        color="#28a745",
    )

    p.add_layout(Legend(items=[("Revenue", [r1]), ("Profit", [r2])]), "right")

    p.yaxis.formatter = NumeralTickFormatter(format="$0,0")
    return p


# ---------------------------------------------------------------------
# Table
# ---------------------------------------------------------------------


@pn.depends(
    year_select.param.value,
    region_select.param.value,
    product_select.param.value,
)
def summary_table(_years, _regions, _products):
    dff = filtered_df()
    if dff.empty:
        return pn.pane.Markdown("No data")

    table = (
        dff.groupby(["year", "month", "region", "product"])
        .agg(
            {
                "revenue": "sum",
                "profit": "sum",
                "units_sold": "sum",
                "profit_margin": "mean",
            }
        )
        .reset_index()
        .sort_values(["year", "month"], ascending=False)
        .head(50)
    )

    return pn.widgets.Tabulator(
        table, pagination="remote", page_size=10, sizing_mode="stretch_width"
    )


# ---------------------------------------------------------------------
# Template
# ---------------------------------------------------------------------

template = pn.template.FastListTemplate(
    title="Sales KPI Dashboard",
    sidebar=[
        pn.pane.Markdown("## Filters"),
        year_select,
        region_select,
        product_select,
        pn.pane.Markdown("## Metric"),
        metric_select,
    ],
    main=[
        kpi_summary,
        pn.Row(trend_chart, yoy_chart),
        pn.Row(region_chart, product_chart),
        sales_rep_chart,
        pn.pane.Markdown("### Monthly Performance"),
        summary_table,
    ],
    header_background="#1565c0",
)

template.servable()
