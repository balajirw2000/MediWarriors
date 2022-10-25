from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def hello(prescription,med,mg,time,notes,name,id,mob):
    pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans-Bold.ttf'))
    c = canvas.Canvas('media/prescription'+id+'.pdf', pagesize=letter)
    width, height = letter
    c.setFont("DejaVu", 12)

    c.drawCentredString(300, 750, "DR address")
    c.drawCentredString(300, 735, "Dr Contact No.")
    c.drawCentredString(300, 720, "Dr details.")

    c.rect(30, 20, 550, 750, stroke=1, fill=0)
    c.rect(60, 645, 240, 60)

    c.setFont("DejaVuSans", 12)
    c.drawString(70, 690, "Patient")

    c.setFont("DejaVu", 10)
    c.drawString(70, 675, name)
    c.setFont("DejaVu", 8)
    c.drawString(70, 665, mob)
    c.drawString(70, 655, id)

    c.setFont("DejaVuSans", 7)
    c.drawString(65, 588, "Prescription")
    c.line(60, 580, 540, 580)
    c.drawString(65, 568, "Medicine")
    c.drawString(180, 568, "Power")
    c.drawString(240, 568, "Doses")
    c.drawString(300, 568, "Notes")

    num = len(list(prescription))
    print("num=",num)
    print(prescription)
    print(list(prescription))
    y1 = 590 - num*45
    for m, p, d, n in zip(med,mg,time,notes):
        y1 = y1 + 45
        y2 = y1-40
        c.setFont("DejaVu", 7)
        c.drawString(65, y2, m)
        c.drawString(180, y2, p)
        c.drawString(240, y2, d)
        for x in range((len(n)//65)+1):
            c.drawString(300, y2, n[65*x:((65)*(x+1))])
            y2 = y2-10

    c.showPage()
    c.save()
    return 1