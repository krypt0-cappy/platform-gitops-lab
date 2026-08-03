package handlers

import (
	"fmt"
	"net/http"
)

func Version(version string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)

		fmt.Fprintf(w, `{"version":%q}`+"\n", version)
	}
}
