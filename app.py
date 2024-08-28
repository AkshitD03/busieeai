from flask import Flask, render_template, request, redirect, url_for
import pytgpt.phind as phind
from pytgpt.imager import Imager
import requests
from PIL import Image
from io import BytesIO
import urllib.parse
import re

app = Flask(__name__)

# Initialize AI models
bot = phind.PHIND()
img = Imager()

def clean_html(content):
    # Remove any unwanted "html" or "```"
    content = re.sub(r"```html|```", "", content)  # Removes markdown-style code blocks
    return content.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if request.method == 'POST':
        # Get the business idea from the form
        query = request.form['business_idea']

        # Generate business name
        name_query = f"This is an idea of business - {query}------. Now generate a cool name for the business. The name should be very deep and meaningful."
        namer = bot.chat(name_query)

        # Generate business description
        desc_query = f"This is an idea of business - {query}------. This is name of the business - {namer}. Now generate a cool description with emojis and attractive text.(generate the output in html form as I am gong to display it in html page dircetly without editing and also do not write anyting the responce.Do not add css to the responce. Make it simple and do add the html in blods of lists only. Write all the headings in h3 tag. DO NOT ADD BUTTONS)"
        descr_raw = bot.chat(desc_query)
        descr = clean_html(descr_raw)  # Clean the raw HTML output

        # Generate MVP
        mvp_query = f"This is an idea of business - {query}------. This is name of the business - {namer}. And this is the description of the business - {descr}. Now generate the MVP for the business.(generate the output in html form as I am gong to display it in html page dircetly without editing and also do not write anyting the responce. Do not add css to the responce. Make it simple and do add the html in blods of lists only. Write all the headings in h3 tag. DO NOT ADD BUTTONS)"
        mvpr = clean_html(bot.chat(mvp_query))  # Cleaning if needed

        # Generate Market Fit
        mf_query = f"This is an idea of business - {query}------. This is name of the business - {namer}. And this is the description of the business - {descr}. Now generate the best Market Fit.(generate the output in html form as I am gong to display it in html page dircetly without editing and also do not write anyting the responceDo not add css to the responce. Make it simple and do add the html in blods of lists only. Write all the headings in h3 tag. DO NOT ADD BUTTONS)"
        mfr = clean_html(bot.chat(mf_query))  # Cleaning if needed

        # Generate Promotion Plan
        pr_query = f"This is an idea of business - {query}------. This is name of the business - {namer}. And this is the description of the business - {descr}. Now generate the best promotion plan.(generate the output in html form as I am gong to display it in html page dircetly without editing and also do not write anyting the responceDo not add css to the responce. Make it simple and do add the html in blods of lists only. Write all the headings in h3 tag. DO NOT ADD BUTTONS)"
        prr = clean_html(bot.chat(pr_query))  # Cleaning if needed

        # Generate Business Model
        bm_query = f"This is an idea of business - {query}------. This is name of the business - {namer}. And this is the description of the business - {descr}. Now generate the best business model.(generate the output in html form as I am gong to display it in html page dircetly without editing and also do not write anyting the responce. Do not add css to the responce. Make it simple and do add the html in blods of lists only. Write all the headings in h3 tag. DO NOT ADD BUTTONS)"
        bmr = clean_html(bot.chat(bm_query))  # Cleaning if needed

        logop = f"This is an idea of business - {query}------. This is name of the business - {namer}. And this is the description of the business - {descr}. Now TEl me how can I MAKE THE BEST UI FOR THE BUSINESS. TELL ME VERY THING, HE ELEMNTS IN THE LOGO,THEME,COLORLS,VEVERYTHING. CTEATE ONLY THE LOGO. DO NOT WRITE ANYTING LESLE BELOW IT(LIKE WE HAVE EXPERITES IN ------, OR SOMETING LIKE THAT, MEANS DO NOT WRITE ANYTING ELSE THE LOGO)"
        logo_query = bot.chat(logop)
        encoded_logo_query = urllib.parse.quote(logo_query)
        logo_url = f"https://image.pollinations.ai/prompt/{encoded_logo_query}"
        response_logo = requests.get(logo_url)
        logo_image = None
        if response_logo.status_code == 200:
            logo_image = "static/logo.png"
            image_logo = Image.open(BytesIO(response_logo.content))
            image_logo.save(logo_image)


        # Generate UI image (asynchronously)
        rui = f"This is an idea of business - {query}------. This is name of the business - {namer}. And this is the description of the business - {descr}. Now generate the best UI FOR THE WEBSITE OF THE BUSINESS."
        ui_query = bot.chat(rui)
        encoded_ui_query = urllib.parse.quote(ui_query)
        ui_url = f"https://image.pollinations.ai/prompt/{encoded_ui_query}"
        response_ui = requests.get(ui_url)
        ui_image = None
        if response_ui.status_code == 200:
            ui_image = "static/ui.png"
            image_ui = Image.open(BytesIO(response_ui.content))
            image_ui.save(ui_image)

        # Generate Marketing Poster
        ad_query = f"Marketing poster for the business called {namer}."
        encoded_ad_query = urllib.parse.quote(ad_query)
        ad_url = f"https://image.pollinations.ai/prompt/{encoded_ad_query}"
        response_ad = requests.get(ad_url)
        ad_image = None
        if response_ad.status_code == 200:
            ad_image = "static/ad.png"
            image_ad = Image.open(BytesIO(response_ad.content))
            image_ad.save(ad_image)

        # Pass data to the result page
        return render_template(
            'result.html',
            business_name=namer,
            description=descr,
            mvp=mvpr,
            market_fit=mfr,
            promotion=prr,
            business_model=bmr,
            logo_image=logo_image,
            ui_image=ui_image,
            ad_image=ad_image
        )

@app.route('/ui_image')
def ui_image():
    return render_template('ui_image.html')

@app.route('/ad_image')
def ad_image():
    return render_template('ad_image.html')

if __name__ == '__main__':
    app.run(debug=True)
