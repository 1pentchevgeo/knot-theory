from links import Link
from tkinter import *
from ast import literal_eval

root = Tk()
# root.geometry("5000x5000")
root.title("Knot Theory Calculator")
icon = Image("photo", file="stevedore_icon.gif")
root.tk.call('wm', 'iconphoto', root.w, icon)


def compute_conway():
    Link.set_deg(degree_slider.get())
    x = literal_eval(input_field.get())
    if type(x) is list:
        x = [x]
    elif type(x) is tuple:
        x = list(x)
    coefficients = Link.from_egc(x).conway()
    first_non_zero = [i for i, j in enumerate(coefficients) if j != 0][0]
    polynomial = ""
    if coefficients[0] != 0:
        polynomial += str(coefficients[0])
    if coefficients[1] != 0:
        if first_non_zero < 1:
            if coefficients[1] > 0:
                polynomial += " + "
            else:
                polynomial += " - "
        if coefficients[1] != 1:
            polynomial += str(abs(coefficients[1]))
        polynomial += "z"
    for i in [i + 2 for i in range(len(coefficients) - 2)]:
        if coefficients[i] != 0:
            if first_non_zero < i:
                if coefficients[i] > 0:
                    polynomial += " + "
                else:
                    polynomial += " - "
            if coefficients[i] != 1:
                polynomial += str(abs(coefficients[i]))
            polynomial += "z^" + str(i)
    output_label["text"] = polynomial


def compute_jones():
    pass


def compute_homfly():
    pass

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

Label(root, text="Enter in the Extended Gauss Code of your link:",
      font=("PT Sans", 24), padx=10, pady=50).grid(row=1, column=1)

input_field = Entry(root, font=("PT Sans", 24), width=40, bd=1)
input_field.grid(row=1, column=2, padx=10)

degree_frame = Frame(root, pady=50)
degree_frame.grid(row=5, column=2)

degree_text = Label(degree_frame, text="Maximum degree of polynomial invariants:", font=("PT Sans", 18))
degree_text.pack()

degree_slider = Scale(degree_frame, from_=2, to_=20, orient=HORIZONTAL, font=("PT Sans", 18), length=200)
degree_slider.set(10)
degree_slider.pack()

polynomial_buttons = Frame(root)
polynomial_buttons.grid(row=4, column=2)

Button(polynomial_buttons, text="Compute Conway polynomial",
       font=("PT Sans", 24), padx=10, pady=5, command=compute_conway).pack(side="top", fill="x", pady=5)

Button(polynomial_buttons, text="Compute Jones polynomial",
       font=("PT Sans", 24), padx=10, pady=5, command=compute_jones, state=DISABLED).pack(side="top", fill="x", pady=5)

Button(polynomial_buttons, text="Compute HOMFLY polynomial",
       font=("PT Sans", 24), padx=10, pady=5, command=compute_homfly, state=DISABLED).pack(side="top", fill="x", pady=5)

output_field = Frame(root)
output_field.grid(row=2, column=2, padx=20, pady=(0, 36))

output_label = Label(output_field, text="",
                     font=("PT Sans", 24), bg="#e6e6e6")
output_label.grid(row=2, column=2)

root.mainloop()
