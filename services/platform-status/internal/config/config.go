package config

import "os"

const (
	defaultAddress = ":8080"
	defaultVersion = "0.1.0"
)

type Config struct {
	Address string
	Version string
}

func Load() Config {
	return Config{
		Address: getEnv("PLATFORM_STATUS_ADDRESS", defaultAddress),
		Version: getEnv("PLATFORM_STATUS_VERSION", defaultVersion),
	}
}

func getEnv(key string, fallback string) string {
	value := os.Getenv(key)

	if value == "" {
		return fallback
	}

	return value
}
