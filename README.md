# CloudStack Usage Web App

This Flask web application interacts with CloudStack to fetch and display usage records based on user inputs such as `domainID`, `start date`, and `end date`.

## Features

- User-friendly input form for `domainID`, `start date`, and `end date`
- Fetches usage records from CloudStack API
- Displays formatted usage records in the browser
- Caches results using Redis for improved performance
- Filters usage records by type
- Aggregates usage data for better readability

## Prerequisites

- Docker
- Docker Compose
- CloudStack API credentials

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/vaheed/cloudstack-usage-webapp.git
   cd cloudstack-usage-webapp
   ```

2. Create a `.env` file in the project root and add your CloudStack API credentials:
   ```
   CLOUDSTACK_API_URL=http://your-cloudstack-api-url
   CLOUDSTACK_ACCESS_KEY=your-access-key
   CLOUDSTACK_SECRET_KEY=your-secret-key
   ```

## Running the Project

1. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```

2. Open your browser and navigate to `http://localhost:5000` to view the web app.

## Usage

1. Enter the Domain ID in the provided field.
2. Select the start and end dates for the usage period.
3. Optionally, select specific usage types to filter the results.
4. Click "Submit" to fetch and display the usage records.

## Project Structure

- `app.py`: Main Flask application file
- `Dockerfile`: Instructions for building the Docker image
- `docker-compose.yml`: Defines and runs the multi-container Docker application
- `requirements.txt`: Lists Python dependencies
- `templates/`: Contains HTML templates for the web interface
- `.env`: Stores environment variables (not tracked in git)
- `.gitignore`: Specifies intentionally untracked files to ignore

## Development

To run the application in development mode:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```bash
   python app.py
   ```

## Troubleshooting

- If you encounter connection issues with CloudStack, ensure your API credentials and URL are correct in the `.env` file.
- For Redis connection errors, make sure the Redis container is running (`docker-compose ps`).

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open-source and free to use. See the LICENSE file for details.
