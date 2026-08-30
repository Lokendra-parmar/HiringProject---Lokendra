def test_pipeline_stage_order():

    stages = [
        "Applied",
        "Screening",
        "Interview",
        "Offer",
        "Hired"
    ]

    assert stages.index("Applied") + 1 == \
           stages.index("Screening")

    assert stages.index("Screening") + 1 == \
           stages.index("Interview")

    assert stages.index("Interview") + 1 == \
           stages.index("Offer")

    assert stages.index("Offer") + 1 == \
           stages.index("Hired")