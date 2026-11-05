# Empório da Música | AI Customer Support Agent

A Python-based AI customer support agent developed for the Artefact AI Engineer Technical Challenge.

The application uses Google's Gemini models, Function Calling, Retrieval-Augmented Generation (RAG), and deterministic Python business rules to assist customers of a fictional musical instrument store.

## Project Overview

The agent supports natural-language conversations in Portuguese and can:

- Search the product catalog by category, price, and availability.
- Calculate promotional prices and PIX discounts without combining incompatible discounts.
- Retrieve store policies from a PDF document using semantic search.
- Check order status, purchased items, and tracking information with customer-level authorization.
- Handle incomplete questions and requests outside the store's scope.

The architecture separates language understanding from data retrieval, pricing calculations, and authorization checks.

## Technical Architecture

The application follows a modular, tool-based architecture.

Google Gemini acts as the conversational interface and decides which available Python function should be executed based on the customer's request and conversation history.

The Python application executes the selected function, applies business rules, and returns structured information to the model.

Gemini then generates a customer-facing response using the retrieved information.

### 1. Language Model

**Provider:** Google Gemini  

**Conversational model:** `gemini-3.5-flash-lite`  

**Python SDK:** `google-genai`

The conversational model is responsible for:

- Interpreting customer requests in Portuguese.
- Maintaining context within an active chat session.
- Selecting appropriate tools through Function Calling.
- Generating clear customer-facing responses.
- Requesting clarification when necessary.

The application uses `Chat.send_message()` with automatic function calling.

Conversation history is maintained in memory during the running session. Persistent conversation storage is not implemented.

### 2. Product Catalog and Pricing

**Technologies:** Python, Pandas, CSV datasets, Decimal

The product tool retrieves information from structured datasets containing products, categories, and promotions.

Business rules are enforced by Python rather than delegated to the language model.

These rules include:

- Returning only active products with available stock.
- Normalizing category names to support common spelling and singular/plural variations.
- Applying active promotional discounts.
- Applying a 5% PIX discount to eligible products.
- Preventing PIX discounts from accumulating with active promotions.
- Filtering products by their final discounted price.

The Gemini model receives the calculated prices instead of performing financial calculations itself.

### 3. Retrieval-Augmented Generation (RAG)

**Technologies:** PyMuPDF, Gemini Embeddings, Scikit-learn  

**Embedding model:** `gemini-embedding-001`

The retrieval pipeline follows these steps:

1. Extract text from the PDF using PyMuPDF.
2. Divide the document into chunks, currently one chunk per page.
3. Generate document embeddings using `RETRIEVAL_DOCUMENT`.
4. Generate question embeddings using `QUESTION_ANSWERING`.
5. Calculate cosine similarity.
6. Retrieve the two highest-ranking chunks.
7. Return the retrieved content to Gemini for response generation.

Document embeddings are cached in memory during the Python process to avoid repeated calculations.

#### Retrieval Strategy Evaluation

Two retrieval methods were evaluated:

- TF-IDF with cosine similarity.
- Gemini semantic embeddings with cosine similarity.

In an exploratory experiment containing three paraphrased questions:

| Retrieval Method | Correct Top-1 Pages |
|---|---:|
| TF-IDF | 1 out of 3 |
| Gemini Embeddings | 3 out of 3 |

Gemini Embeddings was selected as the primary retrieval method based on these initial observations.

This experiment is not a statistically representative benchmark. Further evaluation with more questions is necessary.

### 4. Order Lookup and Authorization

**Technologies:** Python, Pandas, Function Calling

Order information is retrieved by joining orders, order items, and products.

The application checks whether the requested order belongs to the customer identity associated with the session.

The order tool exposed to Gemini accepts only an `order_id`. The customer identifier is bound by the Python application rather than supplied through the model's function arguments.

Unauthorized and nonexistent orders return the same generic error.

**Important:** Authentication is simulated through a local configuration variable. Real authentication and production-grade session management are not implemented.

### 5. Architectural Decisions

The architecture follows three main principles:

**Separation of responsibilities:** Gemini handles natural-language interaction, while Python handles data access and business rules.

**Grounded responses:** Product and policy information is retrieved from the provided data sources.

**Application-level authorization:** Private order access is checked independently of the language model's instructions.

## Installation

### Prerequisites

- Python 3.12
- An internet connection for Gemini API requests
- A Google Gemini API key
- Challenge datasets and policy PDF (included in this repository)

### 1. Clone the Repository

```bash
git clone https://github.com/luizhxavier/artefact-antigravity.git
cd artefact-antigravity
```

Replace `<REPOSITORY_URL>` with the actual GitHub repository URL after publication.

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

The main dependencies are:

- `google-genai`
- `pandas`
- `pymupdf`
- `scikit-learn`
- `python-dotenv`
- `pytest`

The versions used during development are specified in `requirements.txt`.

## Configuration

### Gemini API Key

Create a `.env` file in the project root:

```dotenv
GEMINI_API_KEY=your_gemini_api_key_here
```

The `.env` file is excluded from Git and must not be committed.

### Demonstration Customer Session

For local order-lookup demonstrations, an optional simulated customer identity can be configured:

```dotenv
DEMO_CUSTOMER_ID=your_test_customer_id
```

The value must correspond to a customer with an order in the supplied dataset.

If `DEMO_CUSTOMER_ID` is not configured, the order lookup tool is disabled. Product catalog and policy retrieval features remain available.

**Security warning:** This variable is intended only for local demonstrations. It does not authenticate an actual user and is not suitable for production access control.

## Required Data Files

The project includes the datasets and policy manual provided for the Artefact technical challenge.

All files are available in the `data/` directory:

```text
data/
├── desafio_tecnico_ai_eng - products.csv
├── desafio_tecnico_ai_eng - categories.csv
├── desafio_tecnico_ai_eng - promotions.csv
├── desafio_tecnico_ai_eng - customers.csv
├── desafio_tecnico_ai_eng - orders.csv
├── desafio_tecnico_ai_eng - order_items.csv
└── politicas_da_loja.pdf
```

The datasets represent a fictional musical instrument store and are used for product searches, pricing, promotions, order consultations, and policy retrieval.

No additional data downloads are required to run the project.

To run the agent, create a `.env` file with your own Gemini API key. Set `DEMO_CUSTOMER_ID` only if you want to test order lookup.

## Running the Agent

From the project root, with the virtual environment activated:

```powershell
python -m src.agente
```

The application starts an interactive command-line interface:

```text
=== EMPÓRIO DA MÚSICA ===
Assistente virtual iniciado!
Digite 'sair' para encerrar.
Você:
```

Customers can ask questions about products, prices, discounts, store policies, and, when a demonstration identity is configured, their orders.

Type `sair` to end the session.

## Running Automated Tests

Execute all tests using:

```powershell
python -m pytest -v
```

The development version has 26 automated test cases covering:

- Product search and category normalization.
- Price filtering and stock availability.
- Promotional pricing and PIX discount rules.
- Order lookup and authorization checks.
- Orders with multiple items.
- Missing tracking information.
- Customer-scoped order tools.

The automated tests primarily validate deterministic Python logic.

Conversational behavior and retrieval quality are also evaluated manually through documented examples.

## Conversation Examples

Real observed interactions are documented in the `examples/` directory:

1. [Store Policies with RAG](examples/01_politicas_rag.md)
2. [Product Search and Promotions](examples/02_catalogo_promocoes.md)
3. [Authorized Order Lookup](examples/03_pedidos_autorizacao.md)
4. [Unauthorized Access Attempt](examples/04_seguranca_prompt_injection.md)
5. [Missing Information and Out-of-Scope Requests](examples/05_limites_atendimento.md)

These examples demonstrate tool usage, pricing rules, retrieval behavior, authorization checks, and conversational limitations.

## Prompt Strategy

The system prompt defines the agent's role, communication style, available tools, and response boundaries.

I kept the instructions focused on customer service and the store's business rules. The agent is instructed to consult the appropriate tools, avoid unsupported information, maintain conversation context, and ask for clarification when needed.

I chose to work directly with the Google GenAI SDK instead of using an additional framework such as LangChain. For this project's scope, it provided the necessary Function Calling capabilities while keeping the architecture lightweight and easier to debug.

Pricing calculations, promotional conditions, and order authorization are implemented in Python, so these rules do not depend solely on the LLM following prompt instructions.

## Limitations and Future Improvements

The current implementation covers the main customer service scenarios, but there are some limitations:

- Customer authentication is simulated for order consultations.
- The RAG pipeline uses page-based chunking, which can sometimes retrieve irrelevant content.
- Conversation history is not persisted between sessions.
- The application currently runs through a terminal interface.
- Data is loaded from static CSV snapshots rather than a live store database.

With more time, I would focus on improving the retrieval strategy, expanding the test scenarios, and adding conversation persistence.

I would also expose the agent through a **REST API**, allowing integration with external channels such as **WhatsApp Business**, using webhooks to receive customer messages and return responses.

This would make the solution more practical for a real customer service environment without requiring major changes to the existing business logic.

## AI-Assisted Development

I used **ChatGPT as a development copilot** and **Google Antigravity as my main IDE**.

My approach was to use AI as a collaborative tool throughout the development process, particularly to explore implementation alternatives, translate business requirements into Python logic, review code, investigate errors, and improve test coverage.

For example, I used ChatGPT to discuss how the agent should handle promotional pricing, prevent the accumulation of PIX and promotional discounts, and enforce customer-level authorization for order consultations.

It also helped me evaluate retrieval approaches, organize the project into reusable modules, identify edge cases, and refine the implementation based on actual test results.

My workflow was iterative: define the expected behavior, implement a solution, execute it locally, analyze the results, and make adjustments when necessary.

I used Git to track the project's evolution and Pytest to validate business rules and prevent regressions.

Overall, AI assistance helped accelerate development and supported technical decision-making, while the implementation was continuously validated through local execution and testing.
