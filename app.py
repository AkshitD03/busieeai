from flask import Flask, render_template, request, redirect, url_for
import requests
from PIL import Image
from io import BytesIO
import urllib.parse
import re
from g4f.client import Client

client = Client()

app = Flask(__name__)


def clean_html(content):
    content = re.sub(r"```html|```", "", content)  # Removes markdown-style code blocks
    return content.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if request.method == 'POST':
        query = request.form['business_idea']

        # Generate business name
        name_query = f"This is an idea of business - {query}------. Now generate a cool name for the business. The name should be very deep and meaningful. Give the the name only do not retuen anything else."
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": name_query}]
        )
        namer = response.choices[0].message.content.strip()

        # Generate business description
        desc_query = f"This is an idea of business - {query}------. This is name of the business - {namer}. Now generate a cool description with emojis and attractive text.(generate the output in html form as I am gong to display it in html page directly without editing and also do not write anything else in the response. Do not add css to the response. Make it simple and do add the html in blocks of lists only. Write all the headings in h3 tag. DO NOT ADD BUTTONS)"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": desc_query}]
        )
        descr_raw = response.choices[0].message.content
        descr = clean_html(descr_raw)

        # Generate MVP
        mvp_query = f"This is an idea of business - {query}------. This is name of the business - {namer}. And this is the description of the business - {descr}. Now generate the MVP for the business.(generate the output in html form as I am gong to display it in html page directly without editing and also do not write anything else in the response. Do not add css to the response. Make it simple and do add the html in blocks of lists only. Write all the headings in h3 tag. DO NOT ADD BUTTONS)"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": mvp_query}]
        )
        mvpr = clean_html(response.choices[0].message.content)

        # Generate Market Fit
        mf_query = f"This is an idea of business - {query}------. This is name of the business - {namer}. And this is the description of the business - {descr}. Now generate the best Market Fit.(generate the output in html form as I am gong to display it in html page directly without editing and also do not write anything else in the response. Do not add css to the response. Make it simple and do add the html in blocks of lists only. Write all the headings in h3 tag. DO NOT ADD BUTTONS)"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": mf_query}]
        )
        mfr = clean_html(response.choices[0].message.content)

        # Generate Promotion Plan
        pr_query = f"This is an idea of business - {query}------. This is name of the business - {namer}. And this is the description of the business - {descr}. Now generate the 20 SOCIAL MEDIA POSTS (generate the output in html form as I am gong to display it in html page directly without editing and also do not write anything else in the response. Add css only in border of each social meida Make it simple and do add the html in blocks of lists only. Write all the headings in h3 tag. DO NOT ADD BUTTONS)"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": pr_query}]
        )
        prr = clean_html(response.choices[0].message.content)

        # Generate Business Model
        bm_query = f"This is an idea of business - {query}------. This is name of the business - {namer}. And this is the description of the business - {descr}. Now generate the best business model.(generate the output in html form as I am gong to display it in html page directly without editing and also do not write anything else in the response. Do not add css to the response. Make it simple and do add the html in blocks of lists only. Write all the headings in h3 tag. DO NOT ADD BUTTONS)"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": bm_query}]
        )
        bmr = clean_html(response.choices[0].message.content)


        # Generate Code
        co_query = f"This is an idea of business - {query}------. This is name of the business - {namer}. And this is the description of the business - {descr}. Now generate the frontend of the app using html css and js in 1 html file only. GIVE ME ONLY THE CODE DO NOT WRITE AYTHING ELSE LIKE SURE, OK I AM GIVING, NO JUST CODE IN 1 HTML FILE. "
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": co_query}]
        )
        cor = clean_html(response.choices[0].message.content)


        # Generate logo
        logop = f"This is an idea of business - {query}------. This is name of the business - {namer}. And this is the description of the business - {descr}. Now tell me how can I MAKE THE BEST UI FOR THE BUSINESS. TELL ME EVERYTHING, THE ELEMENTS IN THE LOGO, THEME, COLORS, EVERYTHING. CREATE ONLY THE LOGO. DO NOT WRITE ANYTHING ELSE BELOW IT."
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": logop}]
        )
        logo_query = response.choices[0].message.content
        encoded_logo_query = urllib.parse.quote(logo_query)
        logo_url = f"https://image.pollinations.ai/prompt/{encoded_logo_query}"
        response_logo = requests.get(logo_url)
        logo_image = None
        if response_logo.status_code == 200:
            logo_image = "static/logo.png"
            image_logo = Image.open(BytesIO(response_logo.content))
            image_logo.save(logo_image)

        # Generate UI image
        rui = f"This is an idea of business - {query}------. This is name of the business - {namer}. And this is the description of the business - {descr}. Now generate the best UI FOR THE WEBSITE OF THE BUSINESS."
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": rui}]
        )
        ui_query = response.choices[0].message.content
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
            code=cor,
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
