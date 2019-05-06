import csv

import pdfquery


def get_by_adjacent_element(label, page):
    value = pdf.tree.xpath(
        f'LTPage[@page_index="{page}"]//LTTextBoxHorizontal[normalize-space()="{label}"]/'
        'following::LTTextBoxHorizontal/text()')
    if value:
        return value[0]


def get_by_adjacent_bbox(label_text, page, width=200, height_diff=10):
    label = pdf.pq(f'LTPage[page_index="{page}"] LTTextBoxHorizontal:contains("{label_text}")')
    # Get the coordinates from the label
    if label:
        x1 = float(label.attr('x1'))
        y0 = float(label.attr('y0'))
        y1 = float(label.attr('y1'))
        return pdf.pq(
            f'LTPage[page_index="{page}"] LTTextLineHorizontal:in_bbox("{x1}, {y0 - height_diff}, {x1 + width}, {y1 + height_diff}")').text()


def get_by_bbox(page, x0, y0, x1, y1):
    return pdf.pq(f'LTPage[page_index="{page}"] LTTextBoxHorizontal:in_bbox("{x0}, {y0}, {x1}, {y1}")').text()


if __name__ == '__main__':
    # open the pdf file
    pdf = pdfquery.PDFQuery("sample.pdf")
    # load only the pages from which the data needs to be extracted
    pdf.load(list(range(10, 141)))
    # Prints the pdf tree, useful for getting the coordinates
    # pdf.get_tree(11).write("test2.xml", pretty_print=True, encoding="utf-8")

    # setup to write the output into a csv file.
    with open('noah_investors.csv', 'w', encoding='utf8', newline='') as file:
        writer = None

        for page in range(10, 141):
            item = {
                'company_name': get_by_bbox(page, 230, 470, 230 + 200, 470 + 50),
                'description': get_by_bbox(page, 255, 305, 703, 434),
                'offices': get_by_adjacent_element("Offices", page),
                'active_markets': get_by_adjacent_element("Active Markets", page),
                'founded': get_by_adjacent_element("Founded", page),
                'employees': get_by_adjacent_element("Employees", page),
                'current_fund_size': get_by_adjacent_element("Current Fund Size", page),
                'use_of_debt': get_by_adjacent_element("Use of Debt", page),
                'AUM': get_by_adjacent_element('AUM', page),
                'target_investment_size': get_by_adjacent_element("Target Investment Size", page),
                'target_geographies': get_by_adjacent_element("Target Geographies", page),
                'target_sectors': get_by_adjacent_bbox("Target Sectors", page, height_diff=15),
                'investment_style': get_by_adjacent_element('Investment Style', page),
                'deal_structures': get_by_adjacent_element('Deal Structures', page),
                'key_investment_criteria': get_by_adjacent_bbox('Key Investment Criteria', page),
                'website': get_by_adjacent_element('Website', page),
                'email': get_by_adjacent_element('Contact Email', page),
                'phone': get_by_adjacent_element('Contact Phone', page),
            }
            if not writer:
                writer = csv.DictWriter(file, fieldnames=item.keys())
                writer.writeheader()
            writer.writerow(item)
