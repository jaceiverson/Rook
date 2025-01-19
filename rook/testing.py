from tkinter import *
from PIL import Image, ImageTk


class CardGame:
    def __init__(self, hand):
        self.hand = hand
        self.is_front = True

    def show_hand(self):
        root = Tk()
        root.title("Hand")
        root.resizable(False, False)

        # Frame for the buttons.
        btn_frame = LabelFrame(root)
        btn_frame.grid(row=0, column=1)

        # Frame for the two card images.
        cards_frame = LabelFrame(root, pady=4)
        cards_frame.grid(row=1, column=0, padx=10, pady=5)

        # Frame for the card information.
        info_frame = LabelFrame(root)
        info_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky=W)

        self.cards = []

        for idx, card in enumerate(self.hand):
            self.cards.append(
                Button(cards_frame, command=lambda idx=idx: self.show_back(idx))
            )
            front = Image.open(f"./rook/resources/card-img/{card.short_name}.jpg")
            photo = ImageTk.PhotoImage(front.resize((75, 120), Image.BOX))
            self.cards[idx].config(image=photo)
            self.cards[idx].photo = photo
            self.cards[idx].grid(row=1, column=idx + 1, padx=2, pady=2)

        show_info_button = Button(
            btn_frame, text="Show Card Info", command=self.show_card_info
        )
        show_info_button.pack()

        self.card_info_label = Label(info_frame, text="")
        self.card_info_label.pack(anchor=W)

        root.mainloop()

    def show_back(self, card_index):
        if self.is_front:
            back = Image.open("./rook/resources/card-img/back.jpg")
            photo = ImageTk.PhotoImage(back.resize((75, 120), Image.BOX))
        else:
            card = self.hand[card_index]
            front = Image.open(f"./rook/resources/card-img/{card.short_name}.jpg")
            photo = ImageTk.PhotoImage(front.resize((75, 120), Image.BOX))

        self.cards[card_index].config(image=photo)
        self.cards[card_index].photo = photo

        self.is_front = not self.is_front

    def show_card_info(self):
        visible_cards = [card.short_name() for card in self.hand]
        back_facing_cards = [
            card.short_name() for card in self.hand if not self.is_front
        ]

        card_info = "Visible Cards:\n"
        card_info += "\n".join(visible_cards)
        card_info += "\n\nBack-Facing Cards:\n"
        card_info += "\n".join(back_facing_cards)

        self.card_info_label.config(text=card_info)
