package server

import (
	"log/slog"
	"net/http"

	"github.com/krypt0-cappy/platform-gitops-lab/services/platform-status/internal/config"
	"github.com/krypt0-cappy/platform-gitops-lab/services/platform-status/internal/handlers"
	"github.com/krypt0-cappy/platform-gitops-lab/services/platform-status/internal/middleware"
)

func Run(
	cfg config.Config,
	appLogger *slog.Logger,
) error {
	mux := http.NewServeMux()

	mux.HandleFunc("/", handlers.Home)
	mux.HandleFunc("/health", handlers.Health)
	mux.HandleFunc("/ready", handlers.Ready)
	mux.HandleFunc("/version", handlers.Version(cfg.Version))

	//Temporary test endpoint
	mux.HandleFunc("/panic", func(w http.ResponseWriter, r *http.Request) {
		panic("this is a test panic")
	})

	handler := middleware.Recovery(appLogger, mux)
	handler = middleware.Logging(appLogger, handler)
	handler = middleware.RequestID(handler)

	server := &http.Server{
		Addr:    cfg.Address,
		Handler: handler,
	}

	return server.ListenAndServe()
}
