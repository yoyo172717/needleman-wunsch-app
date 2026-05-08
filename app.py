from flask import Flask, render_template, request, jsonify

aligner = Flask(__name__)


MATCH_REWARD = 1
MISMATCH_PENALTY = -1
GAP_PENALTY = -2


@aligner.route("/")
def landing():
    return render_template("index.html")


def build_matrix(rows, cols):

    return [
        [0 for _ in range(cols)]
        for _ in range(rows)
    ]


def perform_global_alignment(strand_a, strand_b):

    rows = len(strand_a) + 1
    cols = len(strand_b) + 1

    scoring_grid = build_matrix(rows, cols)

    # Initialize edges
    for r in range(rows):
        scoring_grid[r][0] = r * GAP_PENALTY

    for c in range(cols):
        scoring_grid[0][c] = c * GAP_PENALTY

    # Fill matrix
    for r in range(1, rows):

        for c in range(1, cols):

            diagonal_score = scoring_grid[r - 1][c - 1]

            if strand_a[r - 1] == strand_b[c - 1]:
                diagonal_score += MATCH_REWARD
            else:
                diagonal_score += MISMATCH_PENALTY

            upward_score = (
                scoring_grid[r - 1][c]
                + GAP_PENALTY
            )

            leftward_score = (
                scoring_grid[r][c - 1]
                + GAP_PENALTY
            )

            scoring_grid[r][c] = max(
                diagonal_score,
                upward_score,
                leftward_score
            )

    # Traceback
    aligned_a = ""
    aligned_b = ""

    r = len(strand_a)
    c = len(strand_b)

    while r > 0 or c > 0:

        current_score = scoring_grid[r][c]

        if r > 0 and c > 0:

            diagonal_score = scoring_grid[r - 1][c - 1]

            if strand_a[r - 1] == strand_b[c - 1]:
                expected_score = (
                    diagonal_score
                    + MATCH_REWARD
                )
            else:
                expected_score = (
                    diagonal_score
                    + MISMATCH_PENALTY
                )

            if current_score == expected_score:

                aligned_a = strand_a[r - 1] + aligned_a
                aligned_b = strand_b[c - 1] + aligned_b

                r -= 1
                c -= 1

                continue

        if r > 0:

            upward_score = (
                scoring_grid[r - 1][c]
                + GAP_PENALTY
            )

            if current_score == upward_score:

                aligned_a = strand_a[r - 1] + aligned_a
                aligned_b = "-" + aligned_b

                r -= 1

                continue

        aligned_a = "-" + aligned_a
        aligned_b = strand_b[c - 1] + aligned_b

        c -= 1

    return {
        "score": scoring_grid[-1][-1],
        "aligned_a": aligned_a,
        "aligned_b": aligned_b,
        "matrix": scoring_grid
    }


@aligner.route("/align", methods=["POST"])
def align_sequences():

    payload = request.get_json()

    strand_a = (
        payload["sequence_a"]
        .upper()
        .replace(" ", "")
    )

    strand_b = (
        payload["sequence_b"]
        .upper()
        .replace(" ", "")
    )

    alignment_result = perform_global_alignment(
        strand_a,
        strand_b
    )

    return jsonify(alignment_result)


if __name__ == "__main__":
    aligner.run(debug=True)