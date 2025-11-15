"""
Resource Manager - Centralized asset management system.

This module implements the Singleton pattern to provide a centralized,
efficient resource management system for game assets. It handles:
- Image loading with caching to prevent duplicate loads
- Spritesheet parsing and frame extraction
- Multiple path resolution strategies for flexibility
- Memory-efficient asset caching

The ResourceManager follows SOLID principles:
- Single Responsibility: Manages only resource loading and caching
- Open/Closed: Extensible through path strategies without modification
- Dependency Inversion: Uses abstractions (file paths) rather than concrete implementations
"""
import pygame
from typing import Optional, List, Tuple, Dict
from pathlib import Path
import os
import logging

# Configure logging for resource management
logger = logging.getLogger(__name__)


class ResourceManager:
    """
    Singleton resource manager for game assets.
    
    This class implements the Singleton pattern to ensure only one instance
    manages all game resources. It provides efficient caching to prevent
    redundant file I/O operations and memory usage.
    
    The manager uses a multi-strategy path resolution system to find assets
    in various locations, making it flexible for different project structures.
    
    Attributes:
        _instance: Class variable holding the singleton instance
        _initialized: Flag to prevent re-initialization
        _images: Cache dictionary for loaded images
        _spritesheets: Cache dictionary for parsed spritesheets
        assets_dir: Base directory for game assets
    
    Example:
        >>> rm = ResourceManager()
        >>> sprite = rm.load_image("player.png", scale=(64, 64))
        >>> frames = rm.load_spritesheet("enemies.png", 32, 32)
    """
    
    # Class variable for singleton instance
    _instance: Optional['ResourceManager'] = None
    
    # Default configuration
    DEFAULT_ASSETS_DIR = "game"
    
    def __new__(cls) -> 'ResourceManager':
        """
        Create or return the singleton instance.
        
        This method implements the Singleton pattern by ensuring only
        one instance of ResourceManager exists throughout the application.
        
        Returns:
            The singleton ResourceManager instance
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self) -> None:
        """
        Initialize the ResourceManager (only runs once due to singleton).
        
        Sets up the cache dictionaries and configures the assets directory.
        The _initialized flag prevents re-initialization if __init__ is
        called multiple times on the singleton instance.
        """
        if self._initialized:
            return
        
        self._images: Dict[str, pygame.Surface] = {}  # Cache for loaded images
        self._spritesheets: Dict[str, List[pygame.Surface]] = {}  # Cache for spritesheets
        self.assets_dir = self.DEFAULT_ASSETS_DIR  # Main assets folder
        self._initialized = True
        
        logger.info(f"ResourceManager initialized with assets directory: {self.assets_dir}")
    
    def _get_possible_paths(self, filename: str) -> List[str]:
        """
        Generate list of possible file paths to search.
        
        This method implements a multi-strategy path resolution system,
        searching in multiple locations to find the requested asset.
        Paths are ordered by likelihood for performance optimization.
        
        Search strategy (in order):
        1. Direct path in assets directory (game/filename)
        2. Absolute path (filename)
        3. Relative to this module's parent directory
        4. Relative to project root
        
        Args:
            filename: Name or path of the file to locate
            
        Returns:
            List of absolute paths to check in order of priority
        """
        return [
            # Strategy 1: Assets directory (most common)
            os.path.join(self.assets_dir, filename),
            
            # Strategy 2: Direct/absolute path
            filename,
            
            # Strategy 3: Relative to this module's parent directory
            os.path.join(
                os.path.dirname(__file__), 
                '..', 
                '..', 
                self.assets_dir, 
                filename
            ),
            
            # Strategy 4: Project root fallback
            os.path.join(
                os.path.dirname(__file__), 
                '..', 
                '..', 
                filename
            ),
        ]
    
    def load_image(self, filename: str, scale: Optional[Tuple[int, int]] = None, 
                   convert_alpha: bool = True) -> Optional[pygame.Surface]:
        """
        Load an image with caching and automatic format conversion.
        
        This method implements intelligent caching using a composite key
        that includes the filename and transformation parameters. If an
        image with the same parameters has been loaded before, it returns
        the cached version instead of reloading from disk.
        
        The method tries multiple path strategies to locate the file,
        making it flexible for different project structures.
        
        Args:
            filename: Name or path of the image file
            scale: Optional tuple (width, height) to resize the image
            convert_alpha: Whether to convert with alpha channel for transparency
                          Set to True for images with transparency (PNG)
                          Set to False for opaque images (JPG) for better performance
            
        Returns:
            Loaded pygame.Surface or None if file not found
            
        Example:
            >>> rm = ResourceManager()
            >>> sprite = rm.load_image("player.png", scale=(64, 64))
            >>> background = rm.load_image("bg.jpg", convert_alpha=False)
        """
        # Create unique cache key including all transformation parameters
        cache_key = f"{filename}_{scale}_{convert_alpha}"
        
        # Return cached image if available (performance optimization)
        if cache_key in self._images:
            logger.debug(f"Cache hit for image: {filename}")
            return self._images[cache_key]
        
        # Try multiple path strategies to find the file
        paths = self._get_possible_paths(filename)
        # Try multiple path strategies to find the file
        paths = self._get_possible_paths(filename)
        
        img = None
        successful_path = None
        
        for path in paths:
            try:
                # Load image with appropriate conversion
                if convert_alpha:
                    img = pygame.image.load(path).convert_alpha()
                else:
                    img = pygame.image.load(path).convert()
                
                successful_path = path
                logger.debug(f"Successfully loaded image from: {path}")
                break
                
            except (FileNotFoundError, pygame.error) as e:
                # Continue to next path strategy
                logger.debug(f"Failed to load from {path}: {e}")
                continue
        
        # If all paths failed, log error and return None
        if img is None:
            logger.warning(f"Could not load image: {filename} (tried {len(paths)} paths)")
            print(f"⚠️  Could not load image: {filename}")
            return None
        
        # Apply scaling if requested
        if scale:
            try:
                img = pygame.transform.smoothscale(img, scale)
                logger.debug(f"Scaled image {filename} to {scale}")
            except Exception as e:
                logger.error(f"Failed to scale image {filename}: {e}")
                # Return unscaled image rather than None
        
        # Cache the processed image for future use
        self._images[cache_key] = img
        logger.info(f"Cached image: {filename} (cache size: {len(self._images)})")
        
        return img
    
    def load_spritesheet(self, filename: str, frame_width: int, frame_height: int,
                        scale: Optional[Tuple[int, int]] = None) -> List[pygame.Surface]:
        """
        Load and parse a spritesheet into individual frames.
        
        A spritesheet is a single image containing multiple animation frames
        arranged horizontally. This method extracts each frame into a separate
        surface for animation purposes.
        
        The method assumes frames are arranged in a single horizontal row
        and automatically calculates the number of frames based on the
        sheet width and frame width.
        
        Args:
            filename: Name of the spritesheet file
            frame_width: Width of each individual frame in pixels
            frame_height: Height of each frame in pixels
            scale: Optional tuple (width, height) to resize each frame
            
        Returns:
            List of pygame.Surface objects, one per frame.
            Returns empty list if spritesheet cannot be loaded.
            
        Example:
            >>> rm = ResourceManager()
            >>> frames = rm.load_spritesheet("walk.png", 32, 32, scale=(64, 64))
            >>> # frames now contains scaled animation frames
        """
        # Create cache key including all parameters
        cache_key = f"{filename}_{frame_width}_{frame_height}_{scale}"
        
        # Return cached spritesheet if available
        if cache_key in self._spritesheets:
            logger.debug(f"Cache hit for spritesheet: {filename}")
            return self._spritesheets[cache_key]
        
        # Load the full spritesheet image
        sheet = self.load_image(filename, convert_alpha=True)
        if sheet is None:
            logger.error(f"Failed to load spritesheet: {filename}")
            return []
        
        # Calculate number of frames based on sheet dimensions
        sheet_width, sheet_height = sheet.get_size()
        num_frames = sheet_width // frame_width
        frames: List[pygame.Surface] = []
        
        logger.debug(f"Parsing spritesheet {filename}: {num_frames} frames")
        
        # Extract each frame from the sheet
        for col in range(num_frames):
            # Define the rectangle for this frame
            rect = pygame.Rect(
                col * frame_width,  # X position
                0,                   # Y position (assuming single row)
                frame_width,         # Width
                frame_height         # Height
            )
            
            # Create a new surface for this frame with alpha channel
            frame = pygame.Surface(
                (frame_width, frame_height), 
                pygame.SRCALPHA
            )
            
            # Copy the frame from the sheet
            frame.blit(sheet, (0, 0), rect)
            
            # Apply scaling if requested
            if scale:
                frame = pygame.transform.smoothscale(frame, scale)
            
            frames.append(frame)
        
        # Cache the parsed frames
        self._spritesheets[cache_key] = frames
        logger.info(f"Cached spritesheet: {filename} ({len(frames)} frames)")
        
        return frames
    
    def clear_cache(self) -> None:
        """
        Clear all cached resources to free memory.
        
        This method removes all cached images and spritesheets from memory.
        Use this when transitioning between game states or levels to prevent
        memory bloat from unused assets.
        
        Warning:
            After calling this, subsequent load calls will reload from disk.
        """
        image_count = len(self._images)
        sheet_count = len(self._spritesheets)
        
        self._images.clear()
        self._spritesheets.clear()
        
        logger.info(f"Cache cleared: {image_count} images, {sheet_count} spritesheets")
    
    def preload_resources(self, resource_list: List[str]) -> None:
        """
        Preload a list of resources into cache.
        
        This method loads multiple resources at once, typically during a
        loading screen or game initialization. Preloading prevents frame
        drops during gameplay caused by loading assets on-demand.
        
        Args:
            resource_list: List of filenames to preload
            
        Example:
            >>> rm = ResourceManager()
            >>> rm.preload_resources([
            ...     "player.png",
            ...     "enemy1.png",
            ...     "enemy2.png"
            ... ])
        """
        logger.info(f"Preloading {len(resource_list)} resources...")
        
        loaded = 0
        for resource in resource_list:
            if self.load_image(resource) is not None:
                loaded += 1
        
        logger.info(f"Preloaded {loaded}/{len(resource_list)} resources successfully")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get statistics about cached resources.
        
        Returns:
            Dictionary with cache statistics:
            - 'images': Number of cached images
            - 'spritesheets': Number of cached spritesheets
            - 'total': Total cached items
        """
        return {
            'images': len(self._images),
            'spritesheets': len(self._spritesheets),
            'total': len(self._images) + len(self._spritesheets)
        }
    
    def __repr__(self) -> str:
        """
        String representation for debugging.
        
        Returns:
            String showing cache statistics
        """
        stats = self.get_cache_stats()
        return (f"ResourceManager(images={stats['images']}, "
                f"spritesheets={stats['spritesheets']})")


# Global instance for convenient access
resource_manager = ResourceManager()
