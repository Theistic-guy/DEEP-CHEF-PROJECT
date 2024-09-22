# DEEP-CHEF-PROJECT

Image-to-Recipe Web App
This project is a Django-based web application that allows users to upload an image of food and automatically retrieves the recipe for the dish. Our solution combines computer vision, web scraping, and a custom-trained deep learning model to recognize various food items and fetch corresponding recipes.<br><br>

Key Features:

- **Image-to-Recipe Conversion** : Upload an image of a food item, and the app predicts the dish and returns the recipe. We trained a deep learning model using Keras with over 7,000–8,000 images of 380+ different recipes to enable accurate predictions.<br><br>

- **Automated Data Collection** : Used Selenium and ChromeDriver for automated web scraping from Google, downloading images for training, and BeautifulSoup to parse HTML content. We also scraped recipe details from Food.com for a robust recipe dataset.<br><br>

- **Backend and Frontend Development** : Built a responsive and user-friendly web interface using HTML, CSS, Bootstrap, and Django for the backend to seamlessly manage image uploads, predictions, and recipe displays.<br><br>

Technologies Used:
- **Deep Learning** : Keras, TensorFlow for training the image recognition model.<br>
- **Web Scraping** : Selenium, ChromeDriver, BeautifulSoup for collecting images and recipe data.<br>
- **Web Development** : Django, HTML, CSS, Bootstrap for a full-stack application.
