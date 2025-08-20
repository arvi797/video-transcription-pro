#!/bin/bash

# Docker Build Performance Monitor
# This script monitors Docker build performance and provides insights

set -e

echo "🔍 Docker Build Performance Monitor"
echo "=================================="

# Check system resources
echo "📊 System Resources:"
echo "-------------------"
echo "CPU Cores: $(nproc)"
echo "Memory: $(free -h | grep Mem | awk '{print $2}')"
echo "Disk Space:"
df -h | grep -E '^/dev/'

echo ""
echo "🐳 Docker System Info:"
echo "---------------------"
docker system df

echo ""
echo "📦 Docker Images:"
echo "----------------"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"

echo ""
echo "🔧 BuildKit Version:"
echo "-------------------"
docker buildx version

echo ""
echo "💾 Cache Status:"
echo "---------------"
if [ -d "/tmp/.buildx" ]; then
    echo "BuildKit cache directory exists"
    du -sh /tmp/.buildx 2>/dev/null || echo "Cannot access cache directory"
else
    echo "No BuildKit cache directory found"
fi

echo ""
echo "🚀 Build Performance Tips:"
echo "-------------------------"
echo "✅ Use .dockerignore to exclude unnecessary files"
echo "✅ Structure Dockerfile for optimal layer caching"
echo "✅ Use multi-stage builds to reduce final image size"
echo "✅ Pin dependency versions for better cache hits"
echo "✅ Use --no-install-recommends for apt packages"
echo "✅ Clean up caches in the same layer as installs"
echo "✅ Use slimmer base images when possible"
echo "✅ Build for single architecture in CI for speed"

echo ""
echo "📈 Expected Performance Improvements:"
echo "------------------------------------"
echo "• Layer caching: 50-80% faster rebuilds"
echo "• Slimmer base image: 30-50% smaller images"
echo "• Optimized dependencies: 20-40% faster installs"
echo "• Build context reduction: 10-30% faster builds"
