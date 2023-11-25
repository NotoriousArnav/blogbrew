# Bromine Docs
This is Bromine, The Open Source Blog Platform geared towards Developers.
If you reading this Docs, that means you want to Host your Own Instance which is Really great!
Since me ([Arnav Ghosh](https://github.com/NotoriousArnav)), developed this in a Unix Like Environment (I use Arch BTW), so I Really don't reccomend you using Windows for Running Bromine, I mean I did not test it, but if you want you can use Winodws and if it does not work, you can Try WSL too.

## Steps to Run this App!
*Warning!! This is for Linux, Mac, BSD, etc only. To try this, you might need WSL if you are on Windows!*
### Step-1: Grab the Source Files!
```bash
git clone https://gitlab.com/NotoriousArnav/blogbrew.git
```
### Step-2: Make a Virtual Environment and Initialize it (Optional)
This way there is less chance of you messing up Global Dependencies 
```bash
python3 -m venv env --prompt "Bromine"
source env/bin/activate
```
### Step-3: Get your Deps Ready
This might take upto 2 minutes, so please keep patience.
```bash
cd blogbrew
pip3 install -r requirements.txt
```
### Step-4: Generate a Secret SECRET_KEY
Copy the value of the following command, you will need it in Next Step
```bash
python3 -c 'import uuid; print(uuid.uuid4())'
```
### Step-5: Set up .env
Make a .env file and Enter these values:
```
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.serviceprovider.com"
EMAIL_USE_TLS =  True
EMAIL_PORT = "587"
EMAIL_HOST_USER = "youremail@serviceprovider.com"
EMAIL_HOST_PASSWORD = "yourpassword"
SECRET_KEY = 'your-secret-key-from-step-4'
DEBUG = False
DATABASE_URL = "sqlite:///db.sqlite3"
AWS_ACCESS_KEY_ID=''
AWS_SECRET_ACCESS_KEY=''
AWS_S3_ENDPOINT_URL='' #Optional
```

Now here, EMAIL_* Variables are Self-Explanatory, but Let me tell you, these are your Email Creds, so that the app can send email for Account Verfication and Password Reset. Replace serviceprovider.com with your Service Provider like Gmail, or etc. Research what port your Email Service Provider usees and Put that in EMAIL_PORT Variable. At last, put your email id and password in EMAIL_HOST_USER and EMAIL_HOST_PASSWORD.

The SECRET_KEY Variable is the secret key tthat is used for Cyptographic Functions lik Hashing. Its important, so keep that a Secret.

AWS_ACCESS_KEY_ID and AWS_ACCESS_KEY_ID, is something that might be Tricky to Obtain, since many of you are not willing to sign up for AWS. I am using S3 storage (I wont tell which one), and you need one too. You can use Providers like [tebi.io](htps://tebi.io/), to get your Credentials, but keep in Mind, you need to set up the AWS_S3_ENDPOINT_URL to that url of the 3rd Party Provider has provided, in this case Tebi.io (https://s3.tebi.io)

DATABASE_URL is Self-Explanatory. You need to put the URL of your Databse, with the appropriate Protocol. I am Using PostgreSQL, so I had to install psycopg2-binary using pip (`pip install psycopg2-binary`), so In your case you need to see what Dep do you need to clear for your Database. 
*SQL Databases Preferred*

So now after this Hard step, you can Look back and Relax for a Moment

### Step-6: Set up the Database
```bash
python3 makemigrations blogs
python3 makemigrations socialapps_rest_login
python3 migrate
```
Depending on your Database, it might take upto a solid 3 minutes. 

### Step-7: Run
```bash
gunicorn -c gunicorn.conf.py blogsapp.wsgi:app --reload
```
### Congratulations 
If everything you did went Corectly, bromine should be Running Smoothly.

## Maintainers
- [Arnav Ghosh](https://github.com/NotoriousArnav/)
- [Prantik Seal](https://github.com/prantikseal)
- [Bhaskar Mandal](https://github.com/Mbittu00)

