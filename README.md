# chatgpt-analysis

[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/pytorch-2.5.1-orange)](https://pytorch.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**ChatGPT Analysis** is a collection of Jupyter notebooks for exploring and analyzing ChatGPT conversation data. It supports GPU acceleration, zero configuration, and interactive visualizations (to be added).

---

## 🚀 Features

- Load and preprocess your ChatGPT conversation datasets
- Categorize conversations with [sentence-transformers](https://www.sbert.net/) and unsupervised learning methods with [scikit-learn](https://scikit-learn.org/)
- Visualize embeddings and conversation statistics
- Notebook-friendly progress bars (`ipywidgets` or `tqdm.notebook`)
- Compatible with dev containers and GPU-enabled PyTorch

---

## 📂 Project Structure

```
chatgpt-analysis/
├── notebooks/         # Jupyter notebooks
├── scripts/           # Data loading & preprocessing scripts
├── assets/            # Conversation datasets
├── environment.yml    # Conda/Micromamba environment
├── Makefile           # Setup, dev, lint, format commands
└── README.md
```

---

## ⚙️ Installation

1. Clone the repo:

   ```sh
   git clone https://github.com/yourusername/chatgpt-analysis.git
   cd chatgpt-analysis
   ```

2. Install dependencies:

   ```sh
   micromamba env create -f environment.yml
   micromamba activate dev
   ```
3. (Optional) If using VSCode, open the folder in a dev container for a pre-configured environment. 
    - Ensure you have the [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension installed.
    - Open the project folder and select "Reopen in Container" when prompted.
    - This sets up Python, Jupyter, and GPU support automatically.

## 📝 Usage

Start Jupyter Notebook:

```sh
make dev
```

Then open `http://localhost:8888` in your browser to access the notebooks, or use the provided VSCode dev container, with Jupyter support built-in.

## 🛠️ Development

Use the provided Makefile commands for reinstalling, linting and formatting:

- `make install` – Setup environment
- `make lint` – Run Flake8
- `make format` – Run Black

---

## ⚡ Dependencies

- Python 3.11
- PyTorch 2.5.1 + CUDA 12.4
- Sentence Transformers 2.3.1
- pandas, numpy, scipy, scikit-learn
- matplotlib, seaborn
- jupyterlab, notebook, ipywidgets
- black, flake8, isort

---

## 🤝 Contributing

1. Fork the repo and create a feature branch
2. Test notebooks locally
3. Lint & format: `make lint && make format`
4. Submit a pull request

---

## 📜 License

MIT License – see [LICENSE](LICENSE)