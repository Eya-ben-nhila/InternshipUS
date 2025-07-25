package com.example.myapplication.ui.theme

import androidx.compose.ui.graphics.Color

// Main brand color - Yellow from the design
val Primary = Color(0xFFFFC107)

// Dark theme colors
val Background = Color(0xFF121212) // Dark background
val Surface = Color(0xFF1E1E1E) // Slightly lighter surface

// Text and content colors
val OnPrimary = Color.Black
val OnBackground = Color.White
val OnSurface = Color.White.copy(alpha = 0.87f)
val OnSurfaceVariant = Color.White.copy(alpha = 0.6f)

// Additional colors from the design
val EnergyConsumed = Color(0xFFFFC107) // Yellow for consumed energy
val EnergyCapacity = Color(0xFFFFFFFF) // White for capacity text

// Status bar and navigation colors
val StatusBarColor = Color(0xFF000000) // Black for status bar
val NavigationBarColor = Color(0xFF1E1E1E) // Dark surface for navigation
