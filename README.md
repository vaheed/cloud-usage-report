# CloudStack Usage Web App

This is a simple Flask web application that interacts with CloudStack to fetch usage records based on inputs such as `domainID`, `start date`, and `end date`.

## Features

- Input form for `domainID`, `start date`, and `end date`
- Fetches usage records from CloudStack API
- Displays usage records in the browser
- Stores inputs in Redis

## Prerequisites

- Docker
- Docker Compose
- CloudStack API credentials

## Setup

1. Clone this repository or download the ZIP file.
2. Navigate to the project directory.

## Running the Project

1. Update the `.env` file with your CloudStack API URL, access key, and secret key.

```bash
CLOUDSTACK_API_URL=http://your-cloudstack-api-url
CLOUDSTACK_ACCESS_KEY=your-access-key
CLOUDSTACK_SECRET_KEY=your-secret-key
```

2. Build and run the Docker containers:

```bash
docker-compose up --build
```

3. Open your browser and navigate to `http://localhost:5000` to view the web app.

## License

This project is open-source and free to use.
