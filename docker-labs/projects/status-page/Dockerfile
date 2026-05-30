FROM ubuntu:24.04 AS builder

WORKDIR /build
COPY generate-page .
RUN chmod +x generate-page && ./generate-page > index.html

# Run a non-root nginx user
FROM nginxinc/nginx-unprivileged:1.28

# Labels
LABEL org.opencontainers.image.source="https://github.com/joshzee/lab"
LABEL org.opencontainers.image.version="1.0.0"

# Copy HTML
COPY --from=builder /build/index.html /usr/share/nginx/html/index.html

EXPOSE 8080

# Health Check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/ || exit 1
