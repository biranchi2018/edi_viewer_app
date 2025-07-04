def parse_edi_837(edi_text):
    parsed = []
    summary = {
        "Submitter ID": "",
        "Receiver ID": "",
        "Submitter Name": "",
        "Receiver Name": "",
        "Billing Provider Name": "",
        "Billing Provider NPI": "",
        "Billing Provider Tax ID": "",
        "Subscriber Name": "",
        "Subscriber ID": "",
        "Payer Name": "",
        "Payer ID": "",
        "Patient Control Number": "",
        "Claim Amount": "",
        "Claim Frequency": "",
        "Diagnosis Code": "",
        "Service Date": "",
        "Claim Type": "",
        "Referring Provider": "",
        "Referring NPI": "",
        "Original Ref Number": ""
    }

    segments = edi_text.strip().split("~")
    for seg in segments:
        fields = seg.strip().split("*")
        tag = fields[0]
        parsed.append({"segment": tag, "fields": fields[1:]})

        # Submitter/Receiver IDs
        if tag == "ISA" and len(fields) > 8:
            summary["Submitter ID"] = fields[6]
            summary["Receiver ID"] = fields[8]

        # NM1 loops
        elif tag == "NM1" and len(fields) >= 10:
            entity = fields[1]
            if entity == "41":
                summary["Submitter Name"] = fields[3]
            elif entity == "40":
                summary["Receiver Name"] = fields[3]
            elif entity == "85":
                summary["Billing Provider Name"] = fields[3]
                summary["Billing Provider NPI"] = fields[9]
            elif entity == "IL":
                summary["Subscriber Name"] = f"{fields[3]} {fields[4]}"
                summary["Subscriber ID"] = fields[9]
            elif entity == "PR":
                summary["Payer Name"] = fields[3]
                summary["Payer ID"] = fields[9]
            elif entity == "DN":
                summary["Referring Provider"] = fields[3]
                summary["Referring NPI"] = fields[9]

        # REF loops
        elif tag == "REF" and len(fields) >= 2:
            if fields[1] == "EI":
                summary["Billing Provider Tax ID"] = fields[2]
            elif fields[1] == "F8":
                summary["Original Ref Number"] = fields[2]

        # CLM segment
        elif tag == "CLM" and len(fields) >= 6:
            summary["Patient Control Number"] = fields[1]
            summary["Claim Amount"] = fields[2]
            summary["Claim Type"] = fields[5].split(":")[-1]

        # HI segment (diagnosis)
        elif tag == "HI" and len(fields) >= 2:
            summary["Diagnosis Code"] = fields[1].split(":")[-1]

        # DTP (service date)
        elif tag == "DTP" and len(fields) >= 3 and fields[1] == "472":
            summary["Service Date"] = fields[3] if len(fields) > 3 else fields[2]

    return {"segments": parsed, "summary": summary}
