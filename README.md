# ArxivDebate

ArxivDebate is an application designed to extract insightful information from recently published articles on [[arXiv](https://arxiv.org/)](https://arxiv.org/).

## Table of Contents

- [ArxivDebate](#arxivdebate)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Demo](#demo)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Deployment](#deployment)
    - [Docker](#docker)
  - [Contributing](#contributing)

## Features

- **Automated Article Retrieval**: Fetches the latest publications from arXiv based on specified criteria.
- **Insight Extraction**: Processes articles to highlight key insights and significant findings.
- **User-Friendly Interface**: Provides an intuitive interface for users to interact with and explore extracted information.

## Demo

## Installation

To set up the ArxivDebate application locally, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/PooriaT/Arxiv_Debate.git
   cd Arxiv_Debate
   ```

2. **Install Dependencies**:

   This project uses [[Poetry](https://python-poetry.org/)](https://python-poetry.org/) for dependency management.

   If you don't have Poetry installed, you can install it using the following command:

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

   Once Poetry is installed, run:

   ```bash
   poetry install
   ```

3. **Set Up Pre-Commit Hooks** (Optional but recommended):

   This project uses [[pre-commit](https://pre-commit.com/)](https://pre-commit.com/) to maintain code quality.

   To install the pre-commit hooks, run:

   ```bash
   poetry run pre-commit install
   ```

4. **Run the Application**:

   To start the application, use:

   ```bash
   poetry run python app/main.py
   ```

   Replace `app/main.py` with the actual entry point of your application if it differs.

## Usage

Once the application is running, navigate to `http://localhost:8050` (or the specified host and port) in your web browser to access the interface.

From there, you can:

- Specify search criteria to retrieve recent arXiv articles.
- View extracted insights and summaries.
- Interact with the data to explore further details.

## Deployment 

### Docker

## Contributing

Contributions are welcome! If you'd like to contribute to ArxivDebate, please follow these steps:

1. **Fork the Repository**: Click on the 'Fork' button at the top right corner of this page to create a copy of this repository under your GitHub account.

2. **Clone Your Fork**:

   ```bash
   git clone https://github.com/your-username/Arxiv_Debate.git
   cd Arxiv_Debate
   ```

3. **Create a New Branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**: Implement your feature or fix the identified issue.

5. **Run Tests**: Ensure that all tests pass and your changes don't break existing functionality.

6. **Commit Your Changes**:

   ```bash
   git commit -m "Add feature: your feature name"
   ```

7. **Push to Your Fork**:

   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request**: Navigate to the original repository and click on 'New Pull Request' to submit your changes for review.
