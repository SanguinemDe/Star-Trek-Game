"""
Delta-Time Utilities
Helpers for frame-rate independent game logic
"""
import time


class DeltaTimer:
    """
    Manages delta time for frame-rate independent updates.
    
    Usage:
        timer = DeltaTimer()
        
        # Game loop
        while running:
            dt = timer.tick(target_fps=60)
            
            # Update with delta time
            update_game(dt)
    """
    
    def __init__(self):
        self.last_time = time.time()
        self.current_time = self.last_time
        self.delta_time = 0.0
        self.total_time = 0.0
        
        # Performance tracking
        self.frame_count = 0
        self.fps = 0.0
        self.fps_update_timer = 0.0
    
    def tick(self, target_fps=60):
        """
        Calculate delta time since last tick.
        
        Args:
            target_fps: Target frame rate (default: 60)
            
        Returns:
            float: Delta time in seconds
        """
        self.current_time = time.time()
        self.delta_time = self.current_time - self.last_time
        self.last_time = self.current_time
        
        # Cap delta time to prevent huge jumps
        max_dt = 1.0 / target_fps * 3  # Allow 3x frame time max
        if self.delta_time > max_dt:
            self.delta_time = max_dt
        
        self.total_time += self.delta_time
        
        # Update FPS counter
        self.frame_count += 1
        self.fps_update_timer += self.delta_time
        
        if self.fps_update_timer >= 1.0:
            self.fps = self.frame_count / self.fps_update_timer
            self.frame_count = 0
            self.fps_update_timer = 0.0
        
        return self.delta_time
    
    def get_fps(self):
        """Get current FPS"""
        return self.fps
    
    def get_total_time(self):
        """Get total elapsed time"""
        return self.total_time
    
    def reset(self):
        """Reset timer"""
        self.last_time = time.time()
        self.current_time = self.last_time
        self.delta_time = 0.0
        self.total_time = 0.0
        self.frame_count = 0
        self.fps = 0.0
        self.fps_update_timer = 0.0


class Cooldown:
    """
    Delta-time based cooldown timer.
    
    Usage:
        weapon_cooldown = Cooldown(2.0)  # 2 second cooldown
        
        if weapon_cooldown.is_ready():
            fire_weapon()
            weapon_cooldown.start()
        
        # In update loop
        weapon_cooldown.update(dt)
    """
    
    def __init__(self, duration):
        """
        Initialize cooldown.
        
        Args:
            duration: Cooldown duration in seconds
        """
        self.duration = duration
        self.remaining = 0.0
    
    def start(self):
        """Start cooldown"""
        self.remaining = self.duration
    
    def update(self, dt):
        """
        Update cooldown timer.
        
        Args:
            dt: Delta time in seconds
        """
        if self.remaining > 0:
            self.remaining -= dt
            if self.remaining < 0:
                self.remaining = 0
    
    def is_ready(self):
        """Check if cooldown is finished"""
        return self.remaining <= 0
    
    def get_remaining(self):
        """Get remaining cooldown time"""
        return max(0.0, self.remaining)
    
    def get_progress(self):
        """
        Get cooldown progress as percentage.
        
        Returns:
            float: Progress from 0.0 (just started) to 1.0 (ready)
        """
        if self.duration <= 0:
            return 1.0
        return 1.0 - (self.remaining / self.duration)
    
    def reset(self):
        """Reset cooldown to ready state"""
        self.remaining = 0.0
    
    def set_duration(self, new_duration):
        """Change cooldown duration"""
        self.duration = new_duration


class Animation:
    """
    Delta-time based animation helper.
    
    Usage:
        anim = Animation(duration=1.5, loop=False)
        anim.start()
        
        # In update loop
        anim.update(dt)
        progress = anim.get_progress()  # 0.0 to 1.0
        
        # Use progress for interpolation
        position = lerp(start_pos, end_pos, progress)
    """
    
    def __init__(self, duration, loop=False, auto_reverse=False):
        """
        Initialize animation.
        
        Args:
            duration: Animation duration in seconds
            loop: If True, animation loops
            auto_reverse: If True, animation reverses when reaching end
        """
        self.duration = duration
        self.loop = loop
        self.auto_reverse = auto_reverse
        self.time = 0.0
        self.playing = False
        self.direction = 1  # 1 = forward, -1 = reverse
    
    def start(self):
        """Start/restart animation"""
        self.time = 0.0
        self.playing = True
        self.direction = 1
    
    def stop(self):
        """Stop animation"""
        self.playing = False
    
    def pause(self):
        """Pause animation"""
        self.playing = False
    
    def resume(self):
        """Resume animation"""
        self.playing = True
    
    def update(self, dt):
        """
        Update animation.
        
        Args:
            dt: Delta time in seconds
        """
        if not self.playing:
            return
        
        self.time += dt * self.direction
        
        # Handle end of animation
        if self.time >= self.duration:
            if self.auto_reverse:
                self.time = self.duration
                self.direction = -1
            elif self.loop:
                self.time = 0.0
            else:
                self.time = self.duration
                self.playing = False
        
        # Handle reverse reaching start
        if self.auto_reverse and self.time <= 0.0:
            if self.loop:
                self.time = 0.0
                self.direction = 1
            else:
                self.time = 0.0
                self.playing = False
    
    def get_progress(self):
        """
        Get animation progress.
        
        Returns:
            float: Progress from 0.0 to 1.0
        """
        if self.duration <= 0:
            return 1.0
        return max(0.0, min(1.0, self.time / self.duration))
    
    def is_finished(self):
        """Check if animation is complete"""
        return not self.playing and (self.time >= self.duration or self.time <= 0.0)
    
    def is_playing(self):
        """Check if animation is currently playing"""
        return self.playing


def lerp(start, end, t):
    """
    Linear interpolation.
    
    Args:
        start: Start value
        end: End value
        t: Progress from 0.0 to 1.0
        
    Returns:
        Interpolated value
    """
    return start + (end - start) * t


def ease_in_quad(t):
    """Quadratic ease-in (accelerate)"""
    return t * t


def ease_out_quad(t):
    """Quadratic ease-out (decelerate)"""
    return 1.0 - (1.0 - t) * (1.0 - t)


def ease_in_out_quad(t):
    """Quadratic ease-in-out (smooth)"""
    if t < 0.5:
        return 2 * t * t
    else:
        return 1.0 - (-2 * t + 2) ** 2 / 2


def smooth_step(t):
    """Smooth interpolation (smoother than linear)"""
    return t * t * (3.0 - 2.0 * t)


def smoother_step(t):
    """Even smoother interpolation"""
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)


# Example usage
if __name__ == "__main__":
    print("Testing DeltaTimer...")
    timer = DeltaTimer()
    
    # Simulate a few frames
    for i in range(5):
        time.sleep(0.016)  # ~60fps
        dt = timer.tick()
        print(f"Frame {i+1}: dt={dt:.4f}s, FPS={timer.get_fps():.1f}")
    
    print("\nTesting Cooldown...")
    cooldown = Cooldown(1.0)
    cooldown.start()
    
    while not cooldown.is_ready():
        time.sleep(0.1)
        cooldown.update(0.1)
        print(f"Cooldown: {cooldown.get_remaining():.2f}s remaining ({cooldown.get_progress()*100:.0f}% done)")
    
    print("\nTesting Animation...")
    anim = Animation(duration=2.0, loop=False)
    anim.start()
    
    for i in range(21):
        anim.update(0.1)
        progress = anim.get_progress()
        print(f"Frame {i}: Progress={progress:.2f}, Playing={anim.is_playing()}")
    
    print("\nTesting easing functions...")
    for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        print(f"t={t:.2f}: linear={t:.3f}, ease_in={ease_in_quad(t):.3f}, "
              f"ease_out={ease_out_quad(t):.3f}, smooth={smooth_step(t):.3f}")
