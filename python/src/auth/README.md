<div align="center">
  <h3 align="center">Video to MP3 Converter</h3>
</div>

<p>
  A system to convert Videos to MP3s using a microservices architechture 
</p>

## <a name="tech-stack">⚙️ Tech Stack</a>
- Flask
- MySQL
- MongoDB
- RabbitMQ
- Docker
- Kubernetes
- K9s

  ## <a name="architecture">🔋 High Level System Overview</a>

  1. User uploads video to be converted
  2. Request hits API gateway
  3. The gateway stores the video on MongoDB
  4. Gateway places a message on RabbitMQ informing downstream services of the uploaded video
  5. The video to MP3 converter service consumes messages from the RabbitMQ queue
  6. The service extracts the video ID from the message and downloads the video from MongoDB
  7. The video is converted to MP3 and stored on MongoDB
  8. The converter service then puts a new message on the queue 
  9. A notifications service consumes this message and sends a message to the user about the converted file
  10. Client requests the converted file from the API gateway using the unique MP3 ID from notification received 
  11. The API gateway downloads the MP3 from MongoDB and serves the client
  
