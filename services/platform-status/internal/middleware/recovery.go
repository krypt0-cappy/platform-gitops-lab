package middleware

import (
	"log/slog"
	"net/http"
	"runtime/debug"
)

func Recovery(
	appLogger *slog.Logger,
	next http.Handler,
) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			if recovered := recover(); recovered != nil {
				appLogger.Error(
					"Panic recovered",
					"request_id", GetRequestID(r),
					"method", r.Method,
					"path", r.URL.Path,
					"panic", recovered,
					"stack_trace", string(debug.Stack()),
				)

				http.Error(
					w,
					http.StatusText(http.StatusInternalServerError),
					http.StatusInternalServerError,
				)
			}
		}()

		next.ServeHTTP(w, r)
	})
}
