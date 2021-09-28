package com.example.plagiomusicale;

import java.io.Serializable;

public class CheckResults implements Serializable {
    private boolean plagiarism;
    private DataResult dataResult;

    public CheckResults() {
    }

    public CheckResults(boolean plagiarism, DataResult dataResult) {
        this.plagiarism = plagiarism;
        this.dataResult = dataResult;
    }

    public boolean isPlagiarism() {
        return plagiarism;
    }

    public DataResult getDataResult() {
        return dataResult;
    }

    public void setPlagiarism(boolean plagiarism) {
        this.plagiarism = plagiarism;
    }

    public void setDataResult(DataResult dataResult) {
        this.dataResult = dataResult;
    }
}
