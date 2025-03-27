CMillion, I hope you do something awesome with this. If you ever want someone to bounce ideas off of, shoot me an email. Thanks for watching the videos.

# gpt-gerald
Created a talking GPT bot named Gerald.

Set-Up Process:
  - Change your API KEY in the config file

How it works:
  1. Speech to text
  2. Text to GPT
  3. GPT response to my program
  4. Response to Audio
  5. BAM... DONE!
  6. Repeat

What I would like to add:
  - Smoother interface that recognizes when I am done talking and maybe a button that tells it when to start listening in case the user needs time to think of a question (ideally Gerald should just be able to recognize the silence and know not to start talking).


Set Up and Instruction Use Guide with Commands:

#1 Navigate to the directory where you want to store the project (e.g., 'Projects' folder)
cd path\to\desired\location

#2 Clone the repository into that location
git clone https://github.com/evanwaller03/gpt-gerald.git

#3 Navigate into the project directory
cd gpt-gerald

#4 (Optional) Create a virtual environment (if not using one already)
python -m venv venv

#5 Activate the virtual environment
venv\Scripts\activate or source venv/bin/activate (MAC)

#6 Install the required dependencies
pip install -r requirements.txt

#7 Run the project (replace with the actual entry point if different)
python app.py
