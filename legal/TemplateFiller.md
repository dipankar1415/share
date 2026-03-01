# Legal Document Automation Tool

A web-based tool for generating and filling legal documents from templates.

![Legal Document Automation](images/legal-document-automation.png)

## Features

- **PDF Form Filling** - Fill actual PDF forms with data
- **Template Generation** - Create reusable templates from PDFs
- **Preview** - See filled documents before downloading
- **Multiple Formats** - Export as PDF or Word (DOCX)
- **Built-in Templates** - NDA, Service Contract, Will

---

## Quick Start

```bash
cd legal-doc-automation
pip install -r requirements.txt
python app.py
```

Visit: http://localhost:5000

---

## System Architecture

```mermaid
graph LR
    subgraph UI["🖥️ Web Interface"]
        A[Upload PDF]
        B[Fill Form]
        C[Preview]
        D[Download]
    end

    subgraph API["⚙️ Backend API"]
        E[Template Manager]
        F[PDF Processor]
        G[Document Generator]
    end

    subgraph Storage["💾 Storage"]
        H[PDF Templates]
        I[Text Templates]
        J[Output Files]
    end

    A --> E
    B --> F
    E --> H
    E --> I
    F --> G
    G --> J
    J --> C
    C --> D

    style UI fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    style API fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    style Storage fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
```

---

## PDF Form Filling Flow

```mermaid
sequenceDiagram
    participant U as User
    participant W as Web UI
    participant A as API
    participant P as PDF Processor

    U->>W: Upload PDF Form
    W->>A: Send PDF
    A->>P: Extract form fields
    P-->>A: Field names
    A-->>W: Template created
    W-->>U: Show form fields

    U->>W: Fill form data
    W->>A: Submit data
    A->>P: Fill PDF fields
    P-->>A: Filled PDF
    A-->>W: PDF preview
    W-->>U: Display preview

    U->>W: Download
    W->>A: Request file
    A-->>W: PDF file
    W-->>U: Download
```

---

## Document Generation

![Generate Document](images/generate.png)

---

## Template Generation Flow

```mermaid
sequenceDiagram
    participant U as User
    participant W as Web UI
    participant A as API
    participant T as Template Engine

    U->>W: Upload PDF (text mode)
    W->>A: Send PDF
    A->>A: Extract text
    A->>A: Detect fields
    A->>T: Create template
    T-->>A: Template saved
    A-->>W: Template created
    W-->>U: Show detected fields

    U->>W: Fill form data
    W->>A: Submit data
    A->>T: Render template
    T-->>A: Generate PDF
    A-->>W: PDF preview
    W-->>U: Display preview
```

---

## How It Works

```mermaid
graph LR
    subgraph Input["📄 Input"]
        A[PDF with Form Fields]
    end

    subgraph Process["⚙️ Processing"]
        B{Has Form Fields?}
        C[Extract Fields]
        D[Fill PDF Fields]
    end

    subgraph Output["📤 Output"]
        G[Original PDF with Data]
    end

    A --> B
    B -->|Yes| C
    B -->|No| Z[No automation - no fields to fill]
    C --> D
    D --> G

    style Input fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    style Process fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    style Output fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
```

**Key:** PDFs with embedded form fields can be filled automatically. Since there are no fields to fill when the PDF has no form fields, no automation is available in that case.

---

## API Endpoints

| Endpoint          | Method | Description            |
| ----------------- | ------ | ---------------------- |
| `/`               | GET    | Web UI                 |
| `/api/templates`  | GET    | List all templates     |
| `/api/upload-pdf` | POST   | Upload and convert PDF |
| `/api/preview`    | POST   | Generate preview       |
| `/api/generate`   | POST   | Generate and download  |

---

## Project Structure

```
legal-doc-automation/
├── app.py                 # Web server & API
├── document_generator.py  # PDF/DOCX generation
├── pdf_form_filler.py     # PDF form filling
├── pdf_converter.py       # PDF to template
├── field_mapping.py       # Field name mappings
├── templates/             # HTML & Jinja2 templates
├── pdf_templates/         # Uploaded PDF forms
├── static/                # CSS & JavaScript
└── output/                # Generated documents
```

---

## Scripts

| Script                   | Purpose                                     |
| ------------------------ | ------------------------------------------- |
| `clean_templates.py`     | Delete all custom templates                 |
| `create_pdf_template.py` | Create PDF template with proper field names |
| `test_fill_pdf.py`       | Test PDF form filling                       |
| `test_preview.py`        | Test preview generation                     |

---

## License

DipTech Corp.
