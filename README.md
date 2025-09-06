# Generate Exam EVAL API 
Generate Exam EVAL API

<hr>

## `Clone repository`
```bash
git clone https://git.norsys-afrique.dev/ecole-technomacker2024/stscodinhub/generate-exam-syscodinghub.git
```

<hr>

## `Set up environment`
### Install `virtualenv`
```bash
pip install virtualenv
```
### Change current directory to `generate-exam-syscodinghub`
```bash
cd generate-exam-syscodinghub
```
### Create python `virtual environment`
```bash
python -m venv venv
```
### Activate it
- `Windows`
```bash
venv\Scripts\activate
```
- `Linux`
```bash
source venv/Scripts/activate
```
- `PowerShell`
no scripts like the activate script are allowed to be executed so you need to run PowerShell as `admin` and change `ExecutionPolicy` to `AllSigned` then type `A` to `Always run` `the command is under` in the end use `the command above` to activate virtual environment
```bash
Set-ExecutionPolicy AllSigned
```
### Install `virtualenv requirements`
```bash
pip install -r requirements.txt
```
### Run the app
```bash
python run.py
```

# Guide d’installation et de configuration – Application RAG (Ollama + OpenRouter)

Ce guide explique comment installer toutes les dépendances, configurer Ollama, préparer OpenRouter et lancer l’application.

---

## 1. Installer les dépendances Python

Dans un terminal (**Linux**) ou un **PowerShell**/**CMD** (**Windows**), exécutez :

### Installation de PyTorch (version CPU uniquement)

```bash
pip install --no-cache-dir torch==2.3.1+cpu --index-url https://download.pytorch.org/whl/cpu

```
### Installation des autres bibliothèques nécessaires

```bash
pip install \
  langchain==0.3.26 \
  langchain-huggingface==0.3.0 \
  sentence-transformers==5.0.0 \
  transformers==4.53.1 \
  faiss-cpu==1.11.0 \
  python-dotenv==1.1.1 \
  langchain_community \
  jsonschema
```

 Ici, **PyTorch** est installé en version **CPU** uniquement pour éviter le téléchargement des bibliothèques GPU inutiles.

---

## 2. Installer Ollama

### 🔹 Sur **Windows**
1. Téléchargez le fichier `.msi` depuis :  
    [https://ollama.com/download](https://ollama.com/download)
2. Installez-le, puis ouvrez **PowerShell** ou **CMD** et vérifiez :
```bash
ollama --version
```
3. Démarrez le serveur Ollama :
```bash
ollama serve
```

---

### 🔸 Sur **Linux**
1. Installez Ollama :
```bash
curl -fsSL https://ollama.com/install.sh | sh
```
2. Démarrez le serveur Ollama :
```bash
ollama serve
```

---

##  3. Télécharger le modèle Mistral

Ouvrez **un nouveau terminal** et lancez :
```bash
ollama run mistral
```

Cela télécharge et prépare le modèle `mistral:latest` (~4 Go).

---

## 4. Configurer OpenRouter

### 1. Créer un compte OpenRouter
- Rendez-vous sur : [https://openrouter.ai](https://openrouter.ai)
- Créez un compte.

---

### 2. Générer une clé API
- Allez dans la section **Keys**.
- Créez une nouvelle clé.
- Cette clé sera affichée une seul fois **Sauvegardez la!**

---

### 3. Configurer la clé API dans `.env`
Dans la racine du projet, créez un fichier `.env` et ajoutez votre clé API :
```env
OPENROUTER_API_KEY="sk......"
```

---

Le fichier `ai_question_generator/config_ai.py` charge automatiquement ces variables d’environnement.

## 4. Utilisation d’OpenRouter et choix des modèles
Le projet utilise **[OpenRouter](https://openrouter.ai/)** pour interagir avec des modèles de langage (**LLM**) hébergés dans le cloud.  
OpenRouter sert de **passerelle** vers plusieurs fournisseurs (Mistral, OpenAI, Anthropic, Meta, etc.) et permet de changer de modèle sans modifier le code.

### Choix des modèles
Pour ce projet, nous avons retenu :

**Modèles gratuits** :
- `mistralai/mistral-7b-instruct:free` 

**Modèles payants avec quota gratuit** :
- `mistralai/mistral-7b-instruct-v0.3` 

> **Remarque** : OpenRouter offre un **quota gratuit quotidien**.  
> Quand celui-ci est épuisé, vous pouvez :
> - Attendre le lendemain pour récupérer le quota gratuit.
> - Utiliser un **modèle payant** (souvent avec un quota gratuit initial, puis facturation à l’usage).
> - Pour changer le modèle, allez à `ai_question_generator/config_ai.py` :
```python
OPENROUTER_MODEL = "mistralai/mistral-7b-instruct:free" #ICI
# Alternative: "mistralai/mistral-7b-instruct-v0.3" (payant)
```
---
## 5. Lancer l’application

Une fois toutes les étapes ci-dessus terminées, vous pouvez lancer l’application :
```bash
python run.py
```

 Assurez-vous que :
- **Ollama** est démarré (`ollama serve`)
- **Le modèle Mistral** est déjà téléchargé
- **Le fichier `.env`** contient les bonnes clés API

---

# eval
