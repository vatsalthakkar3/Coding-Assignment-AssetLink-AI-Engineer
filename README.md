<div align="center">
  <img fetchpriority="high" width="800" height="156" src="https://assetlink.ai/wp-content/uploads/2023/12/logo-1024x200.webp" class="attachment-large size-large wp-image-213" alt="" srcset="https://assetlink.ai/wp-content/uploads/2023/12/logo-1024x200.webp 1024w, https://assetlink.ai/wp-content/uploads/2023/12/logo-300x59.webp 300w, https://assetlink.ai/wp-content/uploads/2023/12/logo-768x150.webp 768w, https://assetlink.ai/wp-content/uploads/2023/12/logo.webp 1034w" sizes="(max-width: 800px) 100vw, 800px">
</div>

# AssetLink-Coding-Challenge
AssetLink Coding Assignment 

## Prerequisites
You need to have Python installed on your machine. You can download Python from here.

You also need to have Jupyter Notebook installed. If you have Python installed, you can install Jupyter Notebook by running the following command in your terminal:

```bash
pip install notebook
```

## Installing
Clone the repository to your local machine:

```bash
git clone <repository_url>`
```

Navigate to the project directory:
```bash
cd <project_directory>
```

## Installing Dependencies from `requirements.txt`

To install the dependencies directly from the `requirements.txt` file, follow these steps:

1. **Download Miniconda**: Visit the [Miniconda website](https://docs.conda.io/en/latest/miniconda.html) and download the appropriate installer for your operating system.

2. **Install Miniconda**: Follow the installation instructions provided on the Miniconda website after downloading the installer.

3. **Set up Conda Environment**:
    ```bash
    conda create --name AssetLink python=3.11
    ```

4. **Activate the Environment**:
    ```bash
    conda activate AssetLink
    ```

5. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    This command will install all the necessary packages listed in the `requirements.txt` file into your current Python environment.


## Configuration
Rename the .env.example file to .env and fill in the OPENAI_API_KEY and RAPID_API_KEY with your own keys

```bash
OPENAI_API_KEY="your_openai_api_key"
RAPID_API_KEY="your_rapid_api_key"
```

## Running the Project
You can start the Jupyter Notebook server by running the following command in your terminal:

```bash
jupyter notebook
```

This will open the Jupyter Notebook in your default web browser. Navigate to the notebook you want to run and click on it to open it.