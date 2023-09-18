package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strings"

	"github.com/joho/godotenv"
)

const url = "https://api.personal.ai/v1/message"

type Payload struct {
	Text string `json:"Text"`
}

func sendAIMessage(apiKey string, message string) string {
	headers := make(map[string]string)
	headers["Content-Type"] = "application/json"
	headers["x-api-key"] = apiKey

	payload := &Payload{Text: message}
	payloadBytes, err := json.Marshal(payload)
	if err != nil {
		return "Error marshalling payload:" + err.Error()
	}

	resp, err := http.Post(url, "application/json", bytes.NewBuffer(payloadBytes))
	if err != nil {
		return "Error sending request:" + err.Error()
	}
	defer resp.Body.Close()

	var responseData map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&responseData); err != nil {
		return "Error decoding response:" + err.Error()
	}

	fmt.Println("API RESPONSE:", responseData)

	if aiMessage, ok := responseData["ai_message"].(string); ok {
		return aiMessage
	}

	fmt.Println(responseData["ai_message"])

	return "<nil?>"
}

func main() {
	err := godotenv.Load()
	if err != nil {
		fmt.Println(".env not loaded")
		return
	}

	apiKey := os.Getenv("API_KEY")
	if apiKey == "" {
		fmt.Println("API_KEY not set in environment")
		return
	}

	message := strings.Join(os.Args[1:], " ")
	sendAIMessage(apiKey, message)
}
