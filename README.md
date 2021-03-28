# maestro-emporium

## 3-step Technical Excercise

Version `72cf4fe47f85c39779267d0ecee07655a354e623`

### Setup

First, you will need to install `docker` and `docker-compose`. For installation instructions refer to the Docker [docs](https://docs.docker.com/compose/install/)

Second, create a `.env` file in the same directory as the `docker-compose.yml` file and fill it with the data found in `sample.env`

Once these are installed, run `make build` to build the project, then start it up with `make run`.

During the build phase, it will run migrations, run Python tests with coverage, load fixtures and create a superuser. It's no CI/CD, but running the tests prevents the server from booting if there are any issues.

### Run

 - In a terminal, run `make run`
 - Access the site at http://localhost:8000/

### Step 1:

Given:

 - An empty shopping cart
 - And a product, Dove Soap with a unit price of 39.99

When:

 - The user adds 5 Dove Soaps to the shopping cart

Then:

 - The shopping cart should contain 5 Dove Soaps each with a unit price of 39.99
 - And the shopping cart’s total price should equal 199.95

### How to test Step 1:
 1. Build the app, start it with `make run`, then go to the homepage. You will have a button that adds 5 of the 
    requested item to cart. Once that is done, you will be able to see the cart total and number of items on the 
    right of the page
 2. In a terminal, run `make test-python`. This will run a set of tests that are specific to step 1. You can view these
    tests in `shop/tests/test_models.py`