from src.models.job_model import JobModel
import pandas as pd

filename = "src/config/tag_to_categories.xlsx"
df = pd.read_excel(filename, 0)


def postprocess_job_add_categories(job: JobModel):
    df = pd.read_excel(filename, 0)
    categories = []
    for tag in job.tags:
        category = df[df.tags == tag]['Subcategory']
        if category.empty:
            continue
        else:
            category = category.iloc[0]
            categories.append(category)

    if len(categories) == 0:
        categories.append("Others")
    job.job_category = categories
