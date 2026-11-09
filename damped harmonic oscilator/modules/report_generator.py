
"""
Professional PDF Report Generator
Damped Harmonic Oscillator Project
"""

from pathlib import Path
from datetime import datetime

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image
)


def make_table(data, widths=None):

    table = Table(data, colWidths=widths, repeatRows=1)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F2F5F9")),
        ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#222222")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCD5E0")),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("LEADING", (0, 0), (-1, -1), 11),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))

    return table


def add_dataframe(story, dataframe, title, styles):

    if dataframe is None or dataframe.empty:
        return

    story.append(Paragraph(title, styles["Heading2"]))
    story.append(Spacer(1, 5))

    data = [
        [str(column) for column in dataframe.columns]
    ]

    for _, row in dataframe.iterrows():
        data.append([
            str(round(value, 5))
            if isinstance(value, (int, float))
            else str(value)
            for value in row
        ])

    story.append(make_table(data))
    story.append(Spacer(1, 15))


def add_graphs(story, graph_paths, styles):

    if not graph_paths:
        return

    story.append(Paragraph("Scientific Graphs", styles["Heading1"]))
    story.append(Spacer(1, 10))

    for graph_path in graph_paths:

        path = Path(graph_path)

        if path.is_file():

            story.append(
                Paragraph(path.stem.replace("_", " ").title(),
                          styles["Heading3"])
            )

            graph = Image(str(path))

            graph.drawWidth = 155 * mm
            graph.drawHeight = 85 * mm

            story.append(graph)
            story.append(Spacer(1, 12))


def footer(canvas, document):

    canvas.saveState()

    canvas.setStrokeColor(colors.HexColor("#CCD5E0"))
    canvas.line(20 * mm, 15 * mm, 190 * mm, 15 * mm)

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#555555"))

    canvas.drawString(
        20 * mm,
        10 * mm,
        "Damped Harmonic Oscillator - Laboratory Report"
    )

    canvas.drawRightString(
        190 * mm,
        10 * mm,
        f"Page {document.page}"
    )

    canvas.restoreState()


def generate_pdf_report(
    experiment,
    physics_results=None,
    manual_readings=None,
    video_readings=None,
    comparison=None,
    experiment_comparison=None,
    graph_paths=None,
    uncertainty=None,
    student_name="",
    roll_number="",
    output_path="results/oscillator_report.pdf"
):

    Path(output_path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    document = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=22 * mm
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="MainTitle",
        parent=styles["Title"],
        fontSize=25,
        leading=32,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#17365D"),
        spaceAfter=15
    ))

    styles.add(ParagraphStyle(
        name="Subtitle",
        parent=styles["Normal"],
        fontSize=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#526579"),
        spaceAfter=10
    ))

    story = []

    # COVER PAGE

    story.append(Spacer(1, 45 * mm))

    story.append(Paragraph(
        "DAMPED HARMONIC<br/>OSCILLATOR",
        styles["MainTitle"]
    ))

    story.append(Paragraph(
        "Scientific Experimental Analysis Report",
        styles["Subtitle"]
    ))

    story.append(Spacer(1, 20 * mm))

    cover_data = [
        ["DETAIL", "INFORMATION"],
        ["Experiment", str(experiment.get("experiment_name", "N/A"))],
        ["Student", student_name or "Not provided"],
        ["Roll Number", roll_number or "Not provided"],
        ["Medium", str(experiment.get("fluid", "N/A"))],
        ["Shape", str(experiment.get("shape", "N/A"))],
        ["Report Date", datetime.now().strftime("%d-%m-%Y")]
    ]

    story.append(make_table(cover_data, [55 * mm, 105 * mm]))

    story.append(Spacer(1, 25 * mm))

    story.append(Paragraph(
        "Generated using the Damped Harmonic Oscillator "
        "Scientific Analysis Application.",
        styles["Subtitle"]
    ))

    story.append(PageBreak())

    # EXPERIMENT DETAILS

    story.append(Paragraph(
        "1. Experiment Details",
        styles["Heading1"]
    ))

    details = [
        ["Parameter", "Value"],
        ["Experiment", experiment.get("experiment_name", "N/A")],
        ["Mass (kg)", experiment.get("mass_kg", "N/A")],
        ["Spring constant (N/m)",
         experiment.get("spring_constant", "N/A")],
        ["Shape", experiment.get("shape", "N/A")],
        ["Medium", experiment.get("fluid", "N/A")],
        ["Fluid density (kg/m³)",
         experiment.get("fluid_density", "N/A")],
        ["Temperature (°C)",
         experiment.get("temperature", "N/A")]
    ]

    story.append(make_table(details))
    story.append(Spacer(1, 15))

    # PHYSICS RESULTS

    story.append(Paragraph(
        "2. Physics Calculations",
        styles["Heading1"]
    ))

    if physics_results:

        calculation_data = [["Calculation", "Result"]]

        for key, value in physics_results.items():

            calculation_data.append([
                str(key).replace("_", " ").title(),
                str(value)
            ])

        story.append(make_table(calculation_data))

    else:

        story.append(Paragraph(
            "No physics calculation results were supplied.",
            styles["Normal"]
        ))

    story.append(Spacer(1, 15))

    # EXPERIMENTAL READINGS

    story.append(Paragraph(
        "3. Experimental Readings",
        styles["Heading1"]
    ))

    add_dataframe(
        story,
        manual_readings,
        "3.1 Manual Readings",
        styles
    )

    add_dataframe(
        story,
        video_readings,
        "3.2 Video Tracking Readings",
        styles
    )

    # MANUAL VS VIDEO

    story.append(Paragraph(
        "4. Manual vs Video Comparison",
        styles["Heading1"]
    ))

    add_dataframe(
        story,
        comparison,
        "Reading Comparison",
        styles
    )

    # OTHER EXPERIMENTS

    story.append(Paragraph(
        "5. Shape, Mass and Medium Comparison",
        styles["Heading1"]
    ))

    add_dataframe(
        story,
        experiment_comparison,
        "Comparison Results",
        styles
    )

    # UNCERTAINTY

    story.append(Paragraph(
        "6. Measurement Uncertainty",
        styles["Heading1"]
    ))

    if uncertainty:

        uncertainty_data = [["Parameter", "Value"]]

        for key, value in uncertainty.items():
            uncertainty_data.append([str(key), str(value)])

        story.append(make_table(uncertainty_data))

    else:

        story.append(Paragraph(
            "Uncertainty values were not supplied. "
            "No uncertainty has been assumed or invented.",
            styles["Normal"]
        ))

    story.append(Spacer(1, 15))

    # GRAPHS

    story.append(PageBreak())

    story.append(Paragraph(
        "7. Scientific Graphs",
        styles["Heading1"]
    ))

    add_graphs(story, graph_paths, styles)

    # CONCLUSION

    story.append(Paragraph(
        "8. Conclusion",
        styles["Heading1"]
    ))

    story.append(Paragraph(
        "This report presents the configured experiment, "
        "theoretical physics calculations and available "
        "experimental readings. Manual and video measurements "
        "are presented separately wherever supplied. "
        "The comparison results can be used to evaluate "
        "measurement agreement and identify possible "
        "experimental errors.",
        styles["Normal"]
    ))

    story.append(Spacer(1, 20))

    story.append(Paragraph(
        "End of Report",
        styles["Subtitle"]
    ))

    document.build(
        story,
        onFirstPage=footer,
        onLaterPages=footer
    )

    print("\n========== PDF REPORT GENERATED ==========")
    print("Report location:", output_path)

    return output_path
