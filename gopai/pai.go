package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strings"
)

const url = "https://api.personal.ai/v1/message"

type Payload struct {
	Text string `json:"Text"`
}

func sendAIMessage(apiKey string, message string) {
	headers := make(map[string]string)
	headers["Content-Type"] = "application/json"
	headers["x-api-key"] = apiKey

	payload := &Payload{Text: message}
	payloadBytes, err := json.Marshal(payload)
	if err != nil {
		fmt.Println("Error marshalling payload:", err)
		return
	}

	resp, err := http.Post(url, "application/json", bytes.NewBuffer(payloadBytes))
	if err != nil {
		fmt.Println("Error sending request:", err)
		return
	}
	defer resp.Body.Close()

	var responseData map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&responseData); err != nil {
		fmt.Println("Error decoding response:", err)
		return
	}

	fmt.Println()
	fmt.Println(responseData["ai_message"])
}

func main() {
	apiKey := os.Getenv("API_KEY")
	if apiKey == "" {
		fmt.Println("API_KEY not set in environment")
		return
	}

	message := strings.Join(os.Args[1:], " ")
	sendAIMessage(apiKey, message)
}
