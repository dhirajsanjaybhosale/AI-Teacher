"""
Script to create sample educational PDF files for the AI Teacher demo.
"""
import os
import fitz  # PyMuPDF

def create_sample_pdf():
    os.makedirs("sample_data", exist_ok=True)
    pdf_path = os.path.join("sample_data", "cellular_respiration_chapter.pdf")
    
    doc = fitz.open()
    
    # Page 1: Chapter Title & Overview
    page1 = doc.new_page(width=595, height=842) # A4
    page1.insert_text((50, 70), "Chapter 4: Cellular Respiration and Energy Production", fontsize=18, fontname="helv", color=(0.1, 0.2, 0.5))
    page1.insert_text((50, 95), "Department of Biological Sciences — Fundamental Physiology", fontsize=11, fontname="helv", color=(0.4, 0.4, 0.4))
    page1.draw_line((50, 110), (545, 110), color=(0.2, 0.4, 0.7), width=1.5)
    
    body_p1 = """
1. INTRODUCTION TO CELLULAR ENERGY
All living organisms require a continuous supply of energy to drive metabolic processes, maintain homeostasis, and carry out vital biological functions. The universal biochemical energy currency of the cell is Adenosine Triphosphate (ATP). ATP stores potential chemical energy in its high-energy phosphoanhydride bonds. When a cell needs energy, ATP undergoes hydrolysis into Adenosine Diphosphate (ADP) and an inorganic phosphate (Pi), releasing approximately 30.5 kilojoules of usable energy per mole.

Cellular respiration is the comprehensive biochemical pathway by which cells catabolize glucose (C6H12O6) in the presence of oxygen (O2) to synthesize ATP, yielding carbon dioxide (CO2) and water (H2O) as metabolic byproducts:
C6H12O6 + 6 O2 -> 6 CO2 + 6 H2O + ~30-32 ATP molecules.

The complete catabolism of glucose unfolds across four distinct stages:
Stage 1: Glycolysis (occurring in the cytosol)
Stage 2: Pyruvate Oxidation / Link Reaction (mitochondrial matrix)
Stage 3: The Citric Acid Cycle / Krebs Cycle (mitochondrial matrix)
Stage 4: Oxidative Phosphorylation & The Electron Transport Chain (inner mitochondrial membrane)
"""
    page1.insert_textbox(fitz.Rect(50, 125, 545, 800), body_p1.strip(), fontsize=10.5, fontname="times-roman", lineheight=1.4)
    
    # Page 2: Glycolysis & The Krebs Cycle
    page2 = doc.new_page(width=595, height=842)
    page2.insert_text((50, 70), "2. GLYCOLYSIS AND THE CITRIC ACID CYCLE", fontsize=15, fontname="helv", color=(0.1, 0.2, 0.5))
    page2.draw_line((50, 85), (545, 85), color=(0.2, 0.4, 0.7), width=1)
    
    body_p2 = """
2.1 Glycolysis: Splitting the Sugar
Glycolysis is an evolutionary ancient anaerobic pathway that takes place entirely in the cytoplasm (cytosol). It does not require molecular oxygen. During glycolysis, one six-carbon glucose molecule is enzymatically cleaved and oxidized into two three-carbon molecules of pyruvate.
- Energy Investment Phase: The cell consumes 2 molecules of ATP to phosphorylate glucose, destabilizing it.
- Energy Payoff Phase: 4 ATP molecules are synthesized via substrate-level phosphorylation, and 2 molecules of NAD+ are reduced to 2 NADH.
Net Gain of Glycolysis: 2 ATP (net), 2 NADH, and 2 Pyruvate molecules per glucose.

2.2 The Citric Acid (Krebs) Cycle
In the presence of oxygen, pyruvate enters the mitochondrion. It is converted into Acetyl-CoA during the Link Reaction, releasing one CO2 and forming one NADH per pyruvate.
Acetyl-CoA then enters the Citric Acid Cycle in the mitochondrial matrix by combining with oxaloacetate (4-carbon) to form citrate (6-carbon). Through a series of redox reactions, citrate is oxidized back to oxaloacetate.
Key Yield per Glucose (2 turns of the cycle):
- 2 ATP (or GTP) via substrate-level phosphorylation
- 6 NADH electron carriers
- 2 FADH2 electron carriers
- 4 CO2 molecules released as waste
"""
    page2.insert_textbox(fitz.Rect(50, 100, 545, 800), body_p2.strip(), fontsize=10.5, fontname="times-roman", lineheight=1.4)

    # Page 3: Electron Transport Chain & ATP Synthase
    page3 = doc.new_page(width=595, height=842)
    page3.insert_text((50, 70), "3. OXIDATIVE PHOSPHORYLATION & ATP SYNTHASE", fontsize=15, fontname="helv", color=(0.1, 0.2, 0.5))
    page3.draw_line((50, 85), (545, 85), color=(0.2, 0.4, 0.7), width=1)
    
    body_p3 = """
3.1 The Electron Transport Chain (ETC)
The electron transport chain consists of four multiprotein complexes (Complex I, II, III, IV) embedded within the cristae of the inner mitochondrial membrane. NADH and FADH2 donate their high-energy electrons to these complexes.
As electrons transfer down the chain through progressively higher reduction potentials:
- Energy released from redox reactions is harnessed to pump hydrogen ions (protons, H+) across the inner membrane from the matrix into the intermembrane space.
- This creates a steep electrochemical proton gradient known as the Proton-Motive Force (Delta pH and voltage).
- Molecular Oxygen (O2) serves as the final electron acceptor at Complex IV. Oxygen binds electrons and protons to form metabolic water (H2O). Without oxygen, the entire electron chain backs up, stopping aerobic respiration.

3.2 Chemiosmosis and ATP Synthase Turbine
Protons cannot diffuse freely across the lipid bilayer. Instead, they flow down their electrochemical gradient back into the matrix exclusively through the ATP Synthase enzyme complex.
ATP Synthase operates like a microscopic rotary turbine:
1. Proton flow causes the rotor and central stalk to spin.
2. The mechanical rotation induces conformational changes in the catalytic beta subunits of the headpiece.
3. These conformational changes drive the condensation of ADP + Pi into ATP (oxidative phosphorylation).
This chemiosmotic coupling accounts for ~26 to 28 ATP molecules, bringing the total cellular respiration yield to approximately 30-32 ATP per glucose molecule.
"""
    page3.insert_textbox(fitz.Rect(50, 100, 545, 800), body_p3.strip(), fontsize=10.5, fontname="times-roman", lineheight=1.4)
    
    doc.save(pdf_path)
    print(f"Created sample PDF at: {pdf_path} ({len(doc)} pages)")

if __name__ == "__main__":
    create_sample_pdf()
