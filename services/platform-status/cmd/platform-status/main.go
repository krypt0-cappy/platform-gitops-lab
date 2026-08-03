package main

import (
	"os"

	"github.com/krypt0-cappy/platform-gitops-lab/services/platform-status/internal/config"
	"github.com/krypt0-cappy/platform-gitops-lab/services/platform-status/internal/logger"
	"github.com/krypt0-cappy/platform-gitops-lab/services/platform-status/internal/server"
)

func main() {
	cfg := config.Load()
	appLogger := logger.New().With(
    "service", "platform-status",
    "version", cfg.Version,
)

	appLogger.Info(
		"Server starting",
		"address", cfg.Address,
	)

	if err := server.Run(cfg, appLogger); err != nil {
		appLogger.Error(
			"Server stopped unexpectedly",
			"error", err,
		)

		os.Exit(1)
	}
}