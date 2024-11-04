# Resume Tailoring App 📄 

A powerful AI-powered application that helps tailor resumes for specific job descriptions using Google's Gemini AI. Built with Streamlit and Docker.

![image](https://github.com/user-attachments/assets/5a8fc110-3967-4474-a36b-b3ca0de2ae7d)

## 🌟 Features

- **PDF Resume Processing**: Upload and extract text from PDF resumes
- **Job Description Analysis**: Analyze job requirements and match them with resume content
- **AI-Powered Tailoring**: Uses Google's Gemini AI to intelligently modify resumes
- **Project Generation**: Creates relevant projects based on job requirements
- **Format Preservation**: Maintains consistent formatting throughout the modifications
- **Docker Support**: Easy deployment and consistent environment
- **Download Options**: Get your tailored resume in text format

## 🚀 Live Demo

Access the application through Docker:
```bash
docker pull syedmustafa177/resume-tailoring-app:latest
docker run -p 8501:8501 -e GOOGLE_API_KEY=your_google_api_key syedmustafa177/resume-tailoring-app:latest
```
Then visit: http://localhost:8501

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI/ML**: Google Gemini AI
- **PDF Processing**: PDFPlumber
- **Containerization**: Docker
- **CI/CD**: GitHub Actions

## 📋 Prerequisites

- Docker installed on your machine
- Google API Key for Gemini AI
- Python 3.9+ (for local development)

## 🏃‍♂️ Quick Start

### Using Docker (Recommended)

1. Pull the Docker image:
```bash
docker pull syedmustafa177/resume-tailoring-app:latest
```

2. Run the container:
```bash
docker run -p 8501:8501 -e GOOGLE_API_KEY=your_google_api_key syedmustafa177/resume-tailoring-app:latest
```

3. Open your browser and navigate to: http://localhost:8501

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/Syedmustafa177/Resume-Tailoring-App.git
cd Resume-Tailoring-App
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Google API key:
```
GOOGLE_API_KEY=your_google_api_key
```

4. Run the application:
```bash
streamlit run main.py
```

## 📝 Usage Guide

1. **Upload Resume**
   - Click "Upload your current resume (PDF)"
   - Select your PDF resume file

2. **Add Job Description**
   - Paste the job description in the text area
   - Click "Analyze Resume"

3. **Review Analysis**
   - Check the skills alignment
   - Review experience analysis
   - See project recommendations

4. **Generate Enhanced Resume**
   - Click "Generate Enhanced Resume with New Projects"
   - Review the generated content
   - Download the tailored resume

## 🐳 Docker Commands Reference

```bash
# List all images
docker images

# Remove image
docker rmi syedmustafa177/resume-tailoring-app:latest

# Stop all containers
docker stop $(docker ps -a -q)

# Remove all containers
docker rm $(docker ps -a -q)

# Check container logs
docker logs <container_id>
```

## 🔄 CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:
- Automatically builds Docker image on push to main branch
- Pushes image to Docker Hub
- Manages secrets and environment variables
- Ensures consistent deployment

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## 🔒 Security Notes

- Never commit `.env` files
- Keep API keys secure in GitHub Secrets
- Regularly rotate API keys
- Use environment variables in containers

## 🚫 Troubleshooting

Common issues and solutions:

1. **Port 8501 already in use**
   ```bash
   # Use a different port
   docker run -p 8502:8501 -e GOOGLE_API_KEY=your_key syedmustafa177/resume-tailoring-app:latest
   ```

2. **Docker container won't start**
   - Check if Google API key is correctly set
   - Ensure no other containers are using the port
   - Verify Docker service is running

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

- **Syed Mustafa Ali**
- GitHub: [@Syedmustafa177](https://github.com/Syedmustafa177)

## 🙏 Acknowledgments

- Google Gemini AI for powerful language processing
- Streamlit for the amazing web framework
- Docker for containerization support
- GitHub Actions for CI/CD pipeline
