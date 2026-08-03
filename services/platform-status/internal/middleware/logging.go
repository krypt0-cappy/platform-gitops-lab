package middleware

import (
	"log/slog"
	"net/http"
	"time"
)

func Logging(
	appLogger *slog.Logger,
	next http.Handler,
) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()

		requestLogger := appLogger.With(
			"request_id", GetRequestID(r),
			"method", r.Method,
			"path", r.URL.Path,
		)

		requestLogger.Info("HTTP request started")

		rw := &responseWriter{
			ResponseWriter: w,
		}

		next.ServeHTTP(rw, r)

		requestLogger.Info(
			"HTTP request completed",
			"status", rw.status,
			"bytes", rw.bytes,
			"duration_ms", time.Since(start).Milliseconds(),
		)
	})
}
