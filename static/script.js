async function runAlignment() {

    const strandA =
        document.getElementById(
            "strandA"
        ).value;

    const strandB =
        document.getElementById(
            "strandB"
        ).value;


    if (
        !strandA.trim() ||
        !strandB.trim()
    ) {

        alert(
            "Please provide both sequences."
        );

        return;
    }


    const relay = await fetch(
        "/align",
        {

            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({

                sequence_a: strandA,

                sequence_b: strandB
            })
        }
    );


    const alignmentPayload =
        await relay.json();


    document.getElementById(
        "alignmentScore"
    ).innerText =
        alignmentPayload.score;


    document.getElementById(
        "alignedA"
    ).innerText =
        alignmentPayload.aligned_a;


    document.getElementById(
        "alignedB"
    ).innerText =
        alignmentPayload.aligned_b;
}