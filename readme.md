# BufoClicker

BufoClicker is an idle/clicker game built with Pygame, featuring cute frog-like creatures called "bufos". Click to earn bufos, buy buildings for automatic production, upgrade your empire, and unlock achievements!

🎮 [Play the game online now!](https://your-username.github.io/bufoclicker/)

![BufoClicker Screenshot](screenshot.png)

## Features

- 🐸 Click on the bufo to earn bufos
- 🏢 Buy various buildings to generate automatic bufo production
- ⬆️ Purchase upgrades to boost your production
- 🏆 Unlock achievements as you progress
- 🎨 Multiple themes to customize your experience
- ✨ Random golden bufo events for special boosts
- 🎵 Music and sound effects

## How to Play

1. **Click** on the bufo in the center to earn bufos
2. **Buy buildings** to automatically generate bufos over time
3. **Purchase upgrades** to boost your production
4. **Unlock achievements** by reaching milestones
5. **Catch golden bufos** when they appear for temporary boosts
6. **Change themes** to customize your experience

## Building Locally

If you want to run the game locally:

1. Clone the repository:
   ```
   git clone https://github.com/your-username/bufoclicker.git
   cd bufoclicker
   ```

2. Install the required dependencies:
   ```
   pip install pygame
   ```

3. Run the game:
   ```
   python main.py
   ```

## Web Deployment

This game is deployed using [Pygbag](https://github.com/pygame-web/pygbag), which converts Pygame applications to WebAssembly for browser gameplay.

## Development

### Project Structure

```
bufoclicker/
├── assets/           # Game assets folder
├── sounds/           # Game sounds folder
├── src/              # Python source code
│   ├── achievements.py  # Achievement definitions
│   ├── audio.py         # Audio manager
│   ├── boosts.py        # Temporary boosts
│   ├── buildings.py     # Building definitions
│   ├── constants.py     # Game constants
│   ├── game_async.py    # Game logic with async support
│   ├── ui.py            # User interface
│   ├── upgrades.py      # Upgrade definitions
│   └── utils.py         # Utility functions
├── main.py           # Entry point
└── index.html        # For GitHub Pages
```

### Cheat Codes

The game includes several cheat codes for testing or fun:

- `ribbit`: Gain 1,000 bufos
- `hypnobufo`: 10x production for 60 seconds
- `allglory`: Unlock all upgrades
- `todayistuesday`: Gain 1,000,000 bufos

## License

[MIT License](LICENSE)

## Credits

- Created by: Your Name
- Built with: [Pygame](https://www.pygame.org/)
- Web deployment: [Pygbag](https://github.com/pygame-web/pygbag)