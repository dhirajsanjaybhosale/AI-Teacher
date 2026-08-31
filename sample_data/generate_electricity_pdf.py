import fitz

def generate_electricity_pdf():
    pdf_path = "sample_data/sample_chapter.pdf"
    doc = fitz.open()

    # Page 1: Introduction to Voltage, Current, and Resistance
    page1 = doc.new_page(width=595, height=842)
    page1.insert_text((50, 60), "Chapter 5: Fundamentals of Electricity & Ohm's Law", fontsize=16, fontname="helv", color=(0.1, 0.2, 0.5))
    page1.insert_text((50, 80), "Physics & Electrical Engineering Fundamentals", fontsize=10, fontname="helv", color=(0.4, 0.4, 0.4))
    page1.draw_line((50, 95), (545, 95), color=(0.2, 0.4, 0.7), width=1.5)

    body_p1 = """
1. BASIC ELECTRICAL QUANTITIES

Electricity is the flow of electrical charge through a conducting material. To understand how electrical circuits function, three fundamental physical quantities must be understood:

1.1 Voltage (Electric Potential Difference, V)
Voltage, measured in Volts (V), is the electrical pressure or force that pushes electric charges through a conductor. It represents the potential energy difference per unit charge between two points in a circuit. Without voltage, charges remain stationary and no current flows.

1.2 Current (Electric Current, I)
Current, measured in Amperes (A) or Amps, is the rate of flow of electric charge across a cross-section of a conductor over time. One ampere corresponds to one Coulomb of charge passing a point in one second (I = Q / t). Current flows from higher electric potential to lower potential in conventional flow.

1.3 Resistance (Electrical Resistance, R)
Resistance, measured in Ohms (Omega), is the opposition that a material presents to the flow of electric current. Factors affecting resistance include:
- Material resistivity (conductors like copper have low resistance, insulators have high resistance)
- Conductor length (longer conductors have higher resistance)
- Cross-sectional area (thicker wires have lower resistance)
- Temperature (resistance typically increases with temperature in metallic conductors)
"""
    page1.insert_textbox(fitz.Rect(50, 110, 545, 800), body_p1.strip(), fontsize=10, fontname="times-roman", lineheight=1.35)

    # Page 2: Ohm's Law and The Water Pipe Analogy
    page2 = doc.new_page(width=595, height=842)
    page2.insert_text((50, 60), "2. OHM'S LAW AND CIRCUIT MATHEMATICS", fontsize=15, fontname="helv", color=(0.1, 0.2, 0.5))
    page2.draw_line((50, 75), (545, 75), color=(0.2, 0.4, 0.7), width=1)

    body_p2 = """
2.1 The Statement of Ohm's Law
Formulated by German physicist Georg Simon Ohm in 1827, Ohm's Law states that the current (I) flowing through a conductor between two points is directly proportional to the voltage (V) across the two points and inversely proportional to the resistance (R) of the conductor:

Mathematical Formula:
    V = I * R
    I = V / R
    R = V / I

Where:
- V = Voltage in Volts (V)
- I = Current in Amperes (A)
- R = Resistance in Ohms (Omega)

2.2 Physical Implications & Inversion Rule
- Proportionality: If Voltage doubles while Resistance remains constant, Current will double.
- Inverse Proportionality: If Resistance increases while Voltage remains constant, Current DECREASES proportionally.
  Example: If a 12V battery is connected to a 4 Ohm resistor, the current is I = 12 / 4 = 3 Amperes. If resistance is increased to 12 Ohms, the current decreases to I = 12 / 12 = 1 Ampere.

2.3 The Intuitive Water Pipe Analogy
- Voltage is equivalent to water pressure from a pump or elevated water tank.
- Current is equivalent to the volume flow rate of water through the pipe (gallons per minute).
- Resistance is equivalent to a narrow restriction or valve in the pipe. Narrowing the valve (higher resistance) reduces water flow rate (current).
"""
    page2.insert_textbox(fitz.Rect(50, 90, 545, 800), body_p2.strip(), fontsize=10, fontname="times-roman", lineheight=1.35)

    # Page 3: Power and Review Questions
    page3 = doc.new_page(width=595, height=842)
    page3.insert_text((50, 60), "3. ELECTRICAL POWER AND REVIEW QUESTIONS", fontsize=15, fontname="helv", color=(0.1, 0.2, 0.5))
    page3.draw_line((50, 75), (545, 75), color=(0.2, 0.4, 0.7), width=1)

    body_p3 = """
3.1 Electrical Power (P)
Power is the rate at which electrical energy is transferred by an electric circuit per unit time, measured in Watts (W).
Formulas:
- P = V * I
- P = I^2 * R
- P = V^2 / R

3.2 Key Conceptual Summary & Takeaways
1. Voltage pushes charges; Resistance opposes charge flow; Current is the resultant rate of flow.
2. Ohm's Law relates them via I = V / R.
3. Increasing resistance always reduces current when voltage is held constant.

3.3 Check Questions
Q1: What happens to current if resistance increases while voltage remains constant?
Answer: Current decreases (inverse relationship).

Q2: A 9V circuit has a resistance of 3 Ohms. What is the current?
Answer: 3 Amperes (I = 9V / 3 Ohms = 3A).
"""
    page3.insert_textbox(fitz.Rect(50, 90, 545, 800), body_p3.strip(), fontsize=10, fontname="times-roman", lineheight=1.35)

    doc.save(pdf_path)
    print(f"Created {pdf_path}")

if __name__ == "__main__":
    generate_electricity_pdf()
