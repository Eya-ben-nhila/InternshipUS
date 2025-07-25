package com.example.myapplication.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val DarkColorScheme = darkColorScheme(
    primary = Primary,
    onPrimary = OnPrimary,
    background = Background,
    onBackground = OnBackground,
    surface = Surface,
    onSurface = OnSurface,
    surfaceVariant = Surface,
    onSurfaceVariant = OnSurfaceVariant,
    // Custom colors for our app
    primaryContainer = Primary,
    onPrimaryContainer = OnPrimary,
    secondary = Primary,
    onSecondary = OnPrimary,
    secondaryContainer = Primary.copy(alpha = 0.1f),
    onSecondaryContainer = Primary,
    tertiary = Primary,
    onTertiary = OnPrimary,
    error = Color(0xFFFF6E40),
    onError = Color.Black
)

private val LightColorScheme = lightColorScheme(
    primary = Primary,
    onPrimary = OnPrimary,
    background = Color.White,
    onBackground = Color.Black,
    surface = Color.White,
    onSurface = Color.Black,
    surfaceVariant = Color(0xFFEEEEEE),
    onSurfaceVariant = Color(0xFF666666),
    // Custom colors for our app
    primaryContainer = Primary,
    onPrimaryContainer = OnPrimary,
    secondary = Primary,
    onSecondary = OnPrimary,
    secondaryContainer = Primary.copy(alpha = 0.1f),
    onSecondaryContainer = Primary,
    tertiary = Primary,
    onTertiary = OnPrimary,
    error = Color(0xFFD32F2F),
    onError = Color.White
)

@Composable
fun SmartSolarTheme(
    darkTheme: Boolean = true, // Force dark theme for now to match the design
    content: @Composable () -> Unit
) {
    // Always use dark theme for now to match the design
    val colorScheme = DarkColorScheme

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
