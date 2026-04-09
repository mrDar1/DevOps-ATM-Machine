"""2 options for UI: Figma Design or basic.
right now, beutiful Figma has 2 ready screens,
other than that will jump to basic UI (when press admin zone button)"""

# option 1: basic UI
# import ui
# if __name__ == "__main__":
#     ui.ATMApp().run()


# option 2: Figma Design UI (start as Figma and jump to basic_ui when press on admin zone button)
import storage
import figma_ui


def main():
    bank = storage.load_data()
    figma_ui.ATMApp(bank).mainloop()


if __name__ == "__main__":
    main()
