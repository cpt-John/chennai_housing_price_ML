<div id="top"></div>

[![Contributors][contributors-shield]][contributors-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h1 align="center">Chennai House Price Prediction</h1>

  <p align="center">
    A machine learning project using sklearn package with EDA and interactive web-app
    <br />
    <a href="https://chennai-house-price-prediction.herokuapp.com/"><strong><h2>Go to deployed web app »</h2></strong></a>
    <br />
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

This project goes over the full cycle of ML from cleaning the raw data to deployment

Here's what is covered:

- Basic loading and cleaning of the data set
- Useful plots and EDA
- Modeling and Grid Search for fitting the best model
- A web app complete with front end and back end ready for deployment

Use the `model.ipynb` to get started.

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

- [Python 3](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [Seaborn](https://seaborn.pydata.org/)
- [Scikit Learn](https://scikit-learn.org/stable/)
- [Flask](https://flask.palletsprojects.com/en/2.1.x/)
- [HTML](https://html.com/)
- [Javascript](https://www.javascript.com/)
- [JQuery](https://jquery.com)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

Find instructions to install the following software if you are not using web-based interactive computing platform like [Jupyter Notebook](https://jupyter.org/) / [Google Colab](https://colab.research.google.com/?)

- Instructions to install [python](https://wiki.python.org/moin/BeginnersGuide/Download)
- Instructions to install [pip](https://pip.pypa.io/en/stable/installation/)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/cpt-John/chennai_housing_price_ML.git
   ```
2. Install python packages

   ```
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

The `model.ipynb` file discusses the main ideas of data cleaning, plotting and EDA. Towards the end you will find the process of modelling and tuning parameters for best fit . Once you have understood the idea behind the modeling you can checkout the `web_app` directory; This directory contains the files required for the deployment of the project on a server .

### Note :

The web_app directory will contain a `model.joblib` file which is the pickled model to save the time fitting the model during deployment , so delete this file if you want to refit the model

### Steps to start local development server

1. Change directory to `web_app`

2. Start server
   ```
   flask run
   ```

### You can view the deployment on live server here <a href="https://chennai-house-price-prediction.herokuapp.com/"><strong>Go to web app »</strong></a>

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

John Francis - johnfrancis95815@gmail.com

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/cpt-John/chennai_housing_price_ML?style=for-the-badge
[contributors-url]: https://github.com/cpt-John
[license-shield]: https://img.shields.io/github/license/cpt-John/chennai_housing_price_ML?style=for-the-badge
[license-url]: https://github.com/cpt-John/chennai_housing_price_ML/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/john-francis-526999148/
