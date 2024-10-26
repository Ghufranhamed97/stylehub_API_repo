# Test-Endpoints.ps1
# A script to test the Style Hub API endpoints

$baseUrl = "http://localhost:8000"

# Function to make HTTP requests and handle responses
function Invoke-APIRequest {
    param (
        [string]$Method,
        [string]$Endpoint,
        [object]$Body,
        [string]$Token
    )
    
    $headers = @{
        "Content-Type" = "application/json"
    }
    
    if ($Token) {
        $headers["Authorization"] = "Bearer $Token"
    }
    
    $params = @{
        Method = $Method
        Uri = "$baseUrl$Endpoint"
        Headers = $headers
    }
    
    if ($Body) {
        $params["Body"] = ($Body | ConvertTo-Json)
    }
    
    try {
        $response = Invoke-RestMethod @params
        Write-Host "✅ $Method $Endpoint - Success" -ForegroundColor Green
        return $response
    }
    catch {
        Write-Host "❌ $Method $Endpoint - Failed: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

Write-Host "🚀 Starting API endpoint tests..." -ForegroundColor Cyan

# Test 1: API Root
Write-Host "`n📍 Testing API Root" -ForegroundColor Yellow
$rootResponse = Invoke-APIRequest -Method "GET" -Endpoint "/"

# Test 2: User Registration
Write-Host "`n📍 Testing User Registration" -ForegroundColor Yellow
$registerBody = @{
    username = "testuser"
    email = "testuser@example.com"
    password = "TestPass123!"
}
$registerResponse = Invoke-APIRequest -Method "POST" -Endpoint "/users/register/" -Body $registerBody

# Test 3: User Login
Write-Host "`n📍 Testing User Login" -ForegroundColor Yellow
$loginBody = @{
    username = "testuser"
    password = "TestPass123!"
}
$loginResponse = Invoke-APIRequest -Method "POST" -Endpoint "/api/token/" -Body $loginBody

if ($loginResponse) {
    $token = $loginResponse.access
    
    # Test 4: Products List
    Write-Host "`n📍 Testing Products List" -ForegroundColor Yellow
    $productsResponse = Invoke-APIRequest -Method "GET" -Endpoint "/api/products/" -Token $token
    
    # Test 5: Shops List
    Write-Host "`n📍 Testing Shops List" -ForegroundColor Yellow
    $shopsResponse = Invoke-APIRequest -Method "GET" -Endpoint "/api/shops/" -Token $token
    
    # Test 6: Orders List
    Write-Host "`n📍 Testing Orders List" -ForegroundColor Yellow
    $ordersResponse = Invoke-APIRequest -Method "GET" -Endpoint "/api/orders/" -Token $token
    
    # Test 7: User Profile
    Write-Host "`n📍 Testing User Profile" -ForegroundColor Yellow
    $profileResponse = Invoke-APIRequest -Method "GET" -Endpoint "/api/users/" -Token $token
}

Write-Host "`n✨ API endpoint tests completed" -ForegroundColor Cyan