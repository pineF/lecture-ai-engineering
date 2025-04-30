{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "gSpnWBP5ELSI"
      },
      "source": [
        "# 実践演習 Day 1：streamlitとFastAPIのデモ\n",
        "このノートブックでは以下の内容を学習します。\n",
        "\n",
        "- 必要なライブラリのインストールと環境設定\n",
        "- Hugging Faceからモデルを用いたStreamlitのデモアプリ\n",
        "- FastAPIとngrokを使用したAPIの公開方法\n",
        "\n",
        "演習を始める前に、HuggingFaceとngrokのアカウントを作成し、\n",
        "それぞれのAPIトークンを取得する必要があります。\n",
        "\n",
        "\n",
        "演習の時間では、以下の3つのディレクトリを順に説明します。\n",
        "\n",
        "1. 01_streamlit_UI\n",
        "2. 02_streamlit_app\n",
        "3. 03_FastAPI\n",
        "\n",
        "2つ目や3つ目からでも始められる様にノートブックを作成しています。\n",
        "\n",
        "復習の際にもこのノートブックを役立てていただければと思います。\n",
        "\n",
        "### 注意事項\n",
        "「02_streamlit_app」と「03_FastAPI」では、GPUを使用します。\n",
        "\n",
        "これらを実行する際は、Google Colab画面上のメニューから「編集」→ 「ノートブックの設定」\n",
        "\n",
        "「ハードウェアアクセラレーター」の項目の中から、「T4 GPU」を選択してください。\n",
        "\n",
        "このノートブックのデフォルトは「CPU」になっています。\n",
        "\n",
        "---"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "OhtHkJOgELSL"
      },
      "source": [
        "# 環境変数の設定（1~3共有）\n"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "Y-FjBp4MMQHM"
      },
      "source": [
        "GitHubから演習用のコードをCloneします。"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "id": "AIXMavdDEP8U",
        "outputId": "7c523801-ad01-49ba-c82d-4591250aa595",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Cloning into 'lecture-ai-engineering'...\n",
            "remote: Enumerating objects: 52, done.\u001b[K\n",
            "remote: Total 52 (delta 0), reused 0 (delta 0), pack-reused 52 (from 1)\u001b[K\n",
            "Receiving objects: 100% (52/52), 83.21 KiB | 4.89 MiB/s, done.\n",
            "Resolving deltas: 100% (9/9), done.\n"
          ]
        }
      ],
      "source": [
        "!git clone https://github.com/matsuolab/lecture-ai-engineering.git"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "XC8n7yZ_vs1K"
      },
      "source": [
        "必要なAPIトークンを.envに設定します。\n",
        "\n",
        "「lecture-ai-engineering/day1」の配下に、「.env_template」ファイルが存在しています。\n",
        "\n",
        "隠しファイルのため表示されていない場合は、画面左側のある、目のアイコンの「隠しファイルの表示」ボタンを押してください。\n",
        "\n",
        "「.env_template」のファイル名を「.env」に変更します。「.env」ファイルを開くと、以下のような中身になっています。\n",
        "\n",
        "\n",
        "```\n",
        "HUGGINGFACE_TOKEN=\"hf-********\"\n",
        "NGROK_TOKEN=\"********\"\n",
        "```\n",
        "ダブルクオーテーションで囲まれた文字列をHuggingfaceのアクセストークンと、ngrokの認証トークンで書き変えてください。\n",
        "\n",
        "それぞれのアカウントが作成済みであれば、以下のURLからそれぞれのトークンを取得できます。\n",
        "\n",
        "- Huggingfaceのアクセストークン\n",
        "https://huggingface.co/docs/hub/security-tokens\n",
        "\n",
        "- ngrokの認証トークン\n",
        "https://dashboard.ngrok.com/get-started/your-authtoken\n",
        "\n",
        "書き換えたら、「.env」ファイルをローカルのPCにダウンロードしてください。\n",
        "\n",
        "「01_streamlit_UI」から「02_streamlit_app」へ進む際に、CPUからGPUの利用に切り替えるため、セッションが一度切れてしまいます。\n",
        "\n",
        "その際に、トークンを設定した「.env」ファイルは再作成することになるので、その手間を減らすために「.env」ファイルをダウンロードしておくと良いです。"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "Py1BFS5RqcSS"
      },
      "source": [
        "「.env」ファイルを読み込み、環境変数として設定します。次のセルを実行し、最終的に「True」が表示されていればうまく読み込めています。"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 8,
      "metadata": {
        "id": "bvEowFfg5lrq",
        "outputId": "a12d7078-a857-462f-86a3-81b51ee715fb",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: python-dotenv in /usr/local/lib/python3.11/dist-packages (1.1.0)\n",
            "/content/lecture-ai-engineering/day1\n"
          ]
        },
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "True"
            ]
          },
          "metadata": {},
          "execution_count": 8
        }
      ],
      "source": [
        "!pip install python-dotenv\n",
        "from dotenv import load_dotenv, find_dotenv\n",
        "\n",
        "%cd /content/lecture-ai-engineering/day1\n",
        "load_dotenv(find_dotenv())"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "os0Yk6gaELSM"
      },
      "source": [
        "# 01_streamlit_UI\n",
        "\n",
        "ディレクトリ「01_streamlit_UI」に移動します。"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "S28XgOm0ELSM"
      },
      "outputs": [],
      "source": [
        "%cd /content/lecture-ai-engineering/day1/01_streamlit_UI"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "eVp-aEIkELSM"
      },
      "source": [
        "必要なライブラリをインストールします。"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "nBe41LFiELSN"
      },
      "outputs": [],
      "source": [
        "%%capture\n",
        "!pip install -r requirements.txt"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "Yyw6VHaTELSN"
      },
      "source": [
        "ngrokのトークンを使用して、認証を行います。"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "aYw1q0iXELSN"
      },
      "outputs": [],
      "source": [
        "!ngrok authtoken $$NGROK_TOKEN"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "RssTcD_IELSN"
      },
      "source": [
        "アプリを起動します。"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "f-E7ucR6ELSN"
      },
      "outputs": [],
      "source": [
        "from pyngrok import ngrok\n",
        "\n",
        "public_url = ngrok.connect(8501).public_url\n",
        "print(f\"公開URL: {public_url}\")\n",
        "!streamlit run app.py"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "kbYyXVFjELSN"
      },
      "source": [
        "公開URLの後に記載されているURLにブラウザでアクセスすると、streamlitのUIが表示されます。\n",
        "\n",
        "app.pyのコメントアウトされている箇所を編集することで、UIがどの様に変化するか確認してみましょう。\n",
        "\n",
        "streamlitの公式ページには、ギャラリーページがあります。\n",
        "\n",
        "streamlitを使うとpythonという一つの言語であっても、様々なUIを実現できることがわかると思います。\n",
        "\n",
        "https://streamlit.io/gallery"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "MmtP5GLOELSN"
      },
      "source": [
        "後片付けとして、使う必要のないngrokのトンネルを削除します。"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "8Ek9QgahELSO"
      },
      "outputs": [],
      "source": [
        "from pyngrok import ngrok\n",
        "ngrok.kill()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "o-T8tFpyELSO"
      },
      "source": [
        "# 02_streamlit_app"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "QqogFQKnELSO"
      },
      "source": [
        "\n",
        "ディレクトリ「02_streamlit_app」に移動します。"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 14,
      "metadata": {
        "id": "UeEjlJ7uELSO",
        "outputId": "abd5a92e-bd44-49ec-d4b6-c7429aa2a73b",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "/content/lecture-ai-engineering/day1/02_streamlit_app\n"
          ]
        }
      ],
      "source": [
        "%cd /content/lecture-ai-engineering/day1/02_streamlit_app"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "-XUH2AstELSO"
      },
      "source": [
        "必要なライブラリをインストールします。"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 15,
      "metadata": {
        "id": "mDqvI4V3ELSO"
      },
      "outputs": [],
      "source": [
        "%%capture\n",
        "!pip install -r requirements.txt"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "ZO31umGZELSO"
      },
      "source": [
        "ngrokとhuggigfaceのトークンを使用して、認証を行います。"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 16,
      "metadata": {
        "id": "jPxTiEWQELSO",
        "outputId": "dabf0731-cd5b-4757-daea-a6ee10733491",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Authtoken saved to configuration file: /root/.config/ngrok/ngrok.yml\n",
            "The token has not been saved to the git credentials helper. Pass `add_to_git_credential=True` in this function directly or `--add-to-git-credential` if using via `huggingface-cli` if you want to set the git credential as well.\n",
            "Token is valid (permission: read).\n",
            "The token `coffee` has been saved to /root/.cache/huggingface/stored_tokens\n",
            "Your token has been saved to /root/.cache/huggingface/token\n",
            "Login successful.\n",
            "The current active token is: `coffee`\n"
          ]
        }
      ],
      "source": [
        "!ngrok authtoken $$NGROK_TOKEN\n",
        "!huggingface-cli login --token $$HUGGINGFACE_TOKEN"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "dz4WrELLELSP"
      },
      "source": [
        "stramlitでHuggingfaceのトークン情報を扱うために、streamlit用の設定ファイル（.streamlit）を作成し、トークンの情報を格納します。"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 17,
      "metadata": {
        "id": "W184-a7qFP0W"
      },
      "outputs": [],
      "source": [
        "# .streamlit/secrets.toml ファイルを作成\n",
        "import os\n",
        "import toml\n",
        "\n",
        "# 設定ファイルのディレクトリ確保\n",
        "os.makedirs('.streamlit', exist_ok=True)\n",
        "\n",
        "# 環境変数から取得したトークンを設定ファイルに書き込む\n",
        "secrets = {\n",
        "    \"huggingface\": {\n",
        "        \"token\": os.environ.get(\"HUGGINGFACE_TOKEN\", \"\")\n",
        "    }\n",
        "}\n",
        "\n",
        "# 設定ファイルを書き込む\n",
        "with open('.streamlit/secrets.toml', 'w') as f:\n",
        "    toml.dump(secrets, f)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "fK0vI_xKELSP"
      },
      "source": [
        "アプリを起動します。\n",
        "\n",
        "02_streamlit_appでは、Huggingfaceからモデルをダウンロードするため、初回起動には2分程度時間がかかります。\n",
        "\n",
        "この待ち時間を利用して、app.pyのコードを確認してみましょう。"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "TBQyTTWTELSP",
        "outputId": "a6125169-f916-49f0-ef38-fe3937525189",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "公開URL: https://8c29-34-48-37-6.ngrok-free.app\n",
            "\n",
            "Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.\n",
            "\u001b[0m\n",
            "\u001b[0m\n",
            "\u001b[34m\u001b[1m  You can now view your Streamlit app in your browser.\u001b[0m\n",
            "\u001b[0m\n",
            "\u001b[34m  Local URL: \u001b[0m\u001b[1mhttp://localhost:8501\u001b[0m\n",
            "\u001b[34m  Network URL: \u001b[0m\u001b[1mhttp://172.28.0.12:8501\u001b[0m\n",
            "\u001b[34m  External URL: \u001b[0m\u001b[1mhttp://34.48.37.6:8501\u001b[0m\n",
            "\u001b[0m\n",
            "NLTK loaded successfully.\n",
            "2025-04-30 08:10:51.176223: E external/local_xla/xla/stream_executor/cuda/cuda_fft.cc:477] Unable to register cuFFT factory: Attempting to register factory for plugin cuFFT when one has already been registered\n",
            "WARNING: All log messages before absl::InitializeLog() is called are written to STDERR\n",
            "E0000 00:00:1746000651.223767   23047 cuda_dnn.cc:8310] Unable to register cuDNN factory: Attempting to register factory for plugin cuDNN when one has already been registered\n",
            "E0000 00:00:1746000651.238476   23047 cuda_blas.cc:1418] Unable to register cuBLAS factory: Attempting to register factory for plugin cuBLAS when one has already been registered\n",
            "2025-04-30 08:10:51.287107: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.\n",
            "To enable the following instructions: AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.\n",
            "NLTK Punkt data checked/downloaded.\n",
            "Database 'chat_feedback.db' initialized successfully.\n",
            "Data saved to DB successfully.\n",
            "Data saved to DB successfully.\n",
            "Data saved to DB successfully.\n",
            "Data saved to DB successfully.\n",
            "Data saved to DB successfully.\n",
            "Data saved to DB successfully.\n",
            "Data saved to DB successfully.\n",
            "Data saved to DB successfully.\n",
            "Data saved to DB successfully.\n",
            "Data saved to DB successfully.\n",
            "Loading checkpoint shards: 100% 2/2 [00:00<00:00, 17.69it/s]\n",
            "Device set to use cpu\n",
            "2025-04-30 08:11:00.332 Examining the path of torch.classes raised:\n",
            "Traceback (most recent call last):\n",
            "  File \"/usr/local/lib/python3.11/dist-packages/streamlit/web/bootstrap.py\", line 347, in run\n",
            "    if asyncio.get_running_loop().is_running():\n",
            "       ^^^^^^^^^^^^^^^^^^^^^^^^^^\n",
            "RuntimeError: no running event loop\n",
            "\n",
            "During handling of the above exception, another exception occurred:\n",
            "\n",
            "Traceback (most recent call last):\n",
            "  File \"/usr/local/lib/python3.11/dist-packages/streamlit/watcher/local_sources_watcher.py\", line 217, in get_module_paths\n",
            "    potential_paths = extract_paths(module)\n",
            "                      ^^^^^^^^^^^^^^^^^^^^^\n",
            "  File \"/usr/local/lib/python3.11/dist-packages/streamlit/watcher/local_sources_watcher.py\", line 210, in <lambda>\n",
            "    lambda m: list(m.__path__._path),\n",
            "                   ^^^^^^^^^^^^^^^^\n",
            "  File \"/usr/local/lib/python3.11/dist-packages/torch/_classes.py\", line 13, in __getattr__\n",
            "    proxy = torch._C._get_custom_class_python_wrapper(self.name, attr)\n",
            "            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n",
            "RuntimeError: Tried to instantiate class '__path__._path', but it does not exist! Ensure that it is registered via torch::class_\n",
            "NLTK loaded successfully.\n",
            "NLTK Punkt data checked/downloaded.\n",
            "Database 'chat_feedback.db' initialized successfully.\n",
            "2025-04-30 08:12:00.501 Examining the path of torch.classes raised:\n",
            "Traceback (most recent call last):\n",
            "  File \"/usr/local/lib/python3.11/dist-packages/streamlit/web/bootstrap.py\", line 347, in run\n",
            "    if asyncio.get_running_loop().is_running():\n",
            "       ^^^^^^^^^^^^^^^^^^^^^^^^^^\n",
            "RuntimeError: no running event loop\n",
            "\n",
            "During handling of the above exception, another exception occurred:\n",
            "\n",
            "Traceback (most recent call last):\n",
            "  File \"/usr/local/lib/python3.11/dist-packages/streamlit/watcher/local_sources_watcher.py\", line 217, in get_module_paths\n",
            "    potential_paths = extract_paths(module)\n",
            "                      ^^^^^^^^^^^^^^^^^^^^^\n",
            "  File \"/usr/local/lib/python3.11/dist-packages/streamlit/watcher/local_sources_watcher.py\", line 210, in <lambda>\n",
            "    lambda m: list(m.__path__._path),\n",
            "                   ^^^^^^^^^^^^^^^^\n",
            "  File \"/usr/local/lib/python3.11/dist-packages/torch/_classes.py\", line 13, in __getattr__\n",
            "    proxy = torch._C._get_custom_class_python_wrapper(self.name, attr)\n",
            "            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n",
            "RuntimeError: Tried to instantiate class '__path__._path', but it does not exist! Ensure that it is registered via torch::class_\n"
          ]
        }
      ],
      "source": [
        "from pyngrok import ngrok\n",
        "\n",
        "public_url = ngrok.connect(8501).public_url\n",
        "print(f\"公開URL: {public_url}\")\n",
        "!streamlit run app.py"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "8eKWiwzyH0g-"
      },
      "source": [
        "アプリケーションの機能としては、チャット機能や履歴閲覧があります。\n",
        "\n",
        "これらの機能を実現するためには、StreamlitによるUI部分だけではなく、SQLiteを使用したチャット履歴の保存やLLMのモデルを呼び出した推論などの処理を組み合わせることで実現しています。\n",
        "\n",
        "- **`app.py`**: アプリケーションのエントリーポイント。チャット機能、履歴閲覧、サンプルデータ管理のUIを提供します。\n",
        "- **`ui.py`**: チャットページや履歴閲覧ページなど、アプリケーションのUIロジックを管理します。\n",
        "- **`llm.py`**: LLMモデルのロードとテキスト生成を行うモジュール。\n",
        "- **`database.py`**: SQLiteデータベースを使用してチャット履歴やフィードバックを保存・管理します。\n",
        "- **`metrics.py`**: BLEUスコアやコサイン類似度など、回答の評価指標を計算するモジュール。\n",
        "- **`data.py`**: サンプルデータの作成やデータベースの初期化を行うモジュール。\n",
        "- **`config.py`**: アプリケーションの設定（モデル名やデータベースファイル名）を管理します。\n",
        "- **`requirements.txt`**: このアプリケーションを実行するために必要なPythonパッケージ。"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "Xvm8sWFPELSP"
      },
      "source": [
        "後片付けとして、使う必要のないngrokのトンネルを削除します。"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "WFJC2TmZELSP"
      },
      "outputs": [],
      "source": [
        "from pyngrok import ngrok\n",
        "ngrok.kill()"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "rUXhIzV7ELSP"
      },
      "source": [
        "# 03_FastAPI\n",
        "\n",
        "ディレクトリ「03_FastAPI」に移動します。"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 9,
      "metadata": {
        "id": "4ejjDLxr3kfC",
        "outputId": "c55565c6-e459-4e95-fab1-63c9cae55595",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "/content/lecture-ai-engineering/day1/03_FastAPI\n"
          ]
        }
      ],
      "source": [
        "%cd /content/lecture-ai-engineering/day1/03_FastAPI"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "f45TDsNzELSQ"
      },
      "source": [
        "必要なライブラリをインストールします。"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 10,
      "metadata": {
        "id": "9uv6glCz5a7Z"
      },
      "outputs": [],
      "source": [
        "%%capture\n",
        "!pip install -r requirements.txt"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "JfrmE2VmELSQ"
      },
      "source": [
        "ngrokとhuggigfaceのトークンを使用して、認証を行います。"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 11,
      "metadata": {
        "id": "ELzWhMFORRIO",
        "outputId": "c9ea2066-9cf7-4c22-a2da-c980f289beb6",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Authtoken saved to configuration file: /root/.config/ngrok/ngrok.yml\n",
            "The token has not been saved to the git credentials helper. Pass `add_to_git_credential=True` in this function directly or `--add-to-git-credential` if using via `huggingface-cli` if you want to set the git credential as well.\n",
            "Token is valid (permission: read).\n",
            "The token `coffee` has been saved to /root/.cache/huggingface/stored_tokens\n",
            "Your token has been saved to /root/.cache/huggingface/token\n",
            "Login successful.\n",
            "The current active token is: `coffee`\n"
          ]
        }
      ],
      "source": [
        "!ngrok authtoken $$NGROK_TOKEN\n",
        "!huggingface-cli login --token $$HUGGINGFACE_TOKEN"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "t-wztc2CELSQ"
      },
      "source": [
        "アプリを起動します。\n",
        "\n",
        "「02_streamlit_app」から続けて「03_FastAPI」を実行している場合は、モデルのダウンロードが済んでいるため、すぐにサービスが立ち上がります。\n",
        "\n",
        "「03_FastAPI」のみを実行している場合は、初回の起動時にモデルのダウンロードが始まるので、モデルのダウンロードが終わるまで数分間待ちましょう。"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 12,
      "metadata": {
        "id": "meQ4SwISn3IQ",
        "outputId": "ae83f735-a3da-49e6-beed-7b1bf6b4a094",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "2025-04-30 07:46:27.304193: E external/local_xla/xla/stream_executor/cuda/cuda_fft.cc:477] Unable to register cuFFT factory: Attempting to register factory for plugin cuFFT when one has already been registered\n",
            "WARNING: All log messages before absl::InitializeLog() is called are written to STDERR\n",
            "E0000 00:00:1745999187.328594   17099 cuda_dnn.cc:8310] Unable to register cuDNN factory: Attempting to register factory for plugin cuDNN when one has already been registered\n",
            "E0000 00:00:1745999187.335815   17099 cuda_blas.cc:1418] Unable to register cuBLAS factory: Attempting to register factory for plugin cuBLAS when one has already been registered\n",
            "2025-04-30 07:46:27.363290: I tensorflow/core/platform/cpu_feature_guard.cc:210] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.\n",
            "To enable the following instructions: AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.\n",
            "モデル名を設定: google/gemma-2-2b-jpn-it\n",
            "/content/lecture-ai-engineering/day1/03_FastAPI/app.py:134: DeprecationWarning: \n",
            "        on_event is deprecated, use lifespan event handlers instead.\n",
            "\n",
            "        Read more about it in the\n",
            "        [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).\n",
            "        \n",
            "  @app.on_event(\"startup\")\n",
            "FastAPIエンドポイントを定義しました。\n",
            "アクティブなngrokトンネルはありません。\n",
            "ポート8501に新しいngrokトンネルを開いています...\n",
            "---------------------------------------------------------------------\n",
            "✅ 公開URL:   https://7145-34-48-37-6.ngrok-free.app\n",
            "📖 APIドキュメント (Swagger UI): https://7145-34-48-37-6.ngrok-free.app/docs\n",
            "---------------------------------------------------------------------\n",
            "(APIクライアントやブラウザからアクセスするためにこのURLをコピーしてください)\n",
            "\u001b[32mINFO\u001b[0m:     Started server process [\u001b[36m17099\u001b[0m]\n",
            "\u001b[32mINFO\u001b[0m:     Waiting for application startup.\n",
            "load_model_task: モデルの読み込みを開始...\n",
            "使用デバイス: cpu\n",
            "Loading checkpoint shards: 100% 2/2 [00:00<00:00,  9.33it/s]\n",
            "Device set to use cpu\n",
            "モデル 'google/gemma-2-2b-jpn-it' の読み込みに成功しました\n",
            "load_model_task: モデルの読み込みが完了しました。\n",
            "起動時にモデルの初期化が完了しました。\n",
            "\u001b[32mINFO\u001b[0m:     Application startup complete.\n",
            "\u001b[32mINFO\u001b[0m:     Uvicorn running on \u001b[1mhttp://0.0.0.0:8501\u001b[0m (Press CTRL+C to quit)\n",
            "シンプルなリクエストを受信: prompt=こんちは..., max_new_tokens=256\n",
            "モデル推論を開始...\n",
            "モデル推論が完了しました。\n",
            "抽出されたアシスタント応答: ！\n",
            "\n",
            "今日は、ちょっと変わったテーマで、**「好きな音楽と、その音楽が教えてくれる人生のヒント」**についてお話します。\n",
            "\n",
            "音楽は、私たちの人生に深く影響を与えるもの。\n",
            "特定の曲やアーティストを通して...\n",
            "応答生成時間: 227.12秒\n",
            "\u001b[32mINFO\u001b[0m:     35.175.191.123:0 - \"\u001b[1mPOST /generate HTTP/1.1\u001b[0m\" \u001b[32m200 OK\u001b[0m\n",
            "シンプルなリクエストを受信: prompt=こんにちは..., max_new_tokens=256\n",
            "モデル推論を開始...\n",
            "^C\n"
          ]
        }
      ],
      "source": [
        "!python app.py"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "RLubjIhbELSR"
      },
      "source": [
        "FastAPIが起動すると、APIとクライアントが通信するためのURL（エンドポイント）が作られます。\n",
        "\n",
        "URLが作られるのと合わせて、Swagger UIというWebインターフェースが作られます。\n",
        "\n",
        "Swagger UIにアクセスすることで、APIの仕様を確認できたり、APIをテストすることができます。\n",
        "\n",
        "Swagger UIを利用することで、APIを通してLLMを動かしてみましょう。"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "XgumW3mGELSR"
      },
      "source": [
        "後片付けとして、使う必要のないngrokのトンネルを削除します。"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 13,
      "metadata": {
        "id": "RJymTZio-WPJ"
      },
      "outputs": [],
      "source": [
        "from pyngrok import ngrok\n",
        "ngrok.kill()"
      ]
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "SSfQgXjxvgoK"
      },
      "execution_count": null,
      "outputs": []
    }
  ],
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}