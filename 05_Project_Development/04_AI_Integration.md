# AI Integration

## AI Integration

EduGenie uses an AI service to generate simple and understandable answers for student questions.

## AI Processing Flow

1. User enters a question.
2. The question is sent to the Python backend.
3. The backend sends the question to the AI API.
4. The AI service processes the question.
5. An AI-generated response is returned.
6. The response is displayed to the user.

## API Key Security

The AI API key should be stored in an environment variable such as `.env`.

The API key must not be written directly in the source code or uploaded to GitHub.

## Error Handling

If the AI service is unavailable or an API error occurs, the application should display a suitable error message.

## Expected Result

The AI integration should provide students with useful explanations and learning support.