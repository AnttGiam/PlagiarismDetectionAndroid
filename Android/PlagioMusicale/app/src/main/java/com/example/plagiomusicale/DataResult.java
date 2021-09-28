package com.example.plagiomusicale;

import java.io.Serializable;

public class DataResult implements Serializable {
    private String file_not_found,cosine,soresen_dice,overlap,clustering,clusteringValue,percentuage,threshold;

    public DataResult() {
    }

    public DataResult(String file_not_found, String cosine, String soresen_dice, String overlap, String clustering, String clusteringValue, String percentuage, String threshold) {
        this.file_not_found = file_not_found;
        this.cosine = cosine;
        this.soresen_dice = soresen_dice;
        this.overlap = overlap;
        this.clustering = clustering;
        this.clusteringValue = clusteringValue;
        this.percentuage = percentuage;
        this.threshold = threshold;
    }

    public String getFile_not_found() {
        return file_not_found;
    }

    public String getCosine() {
        return cosine;
    }

    public String getSoresen_dice() {
        return soresen_dice;
    }

    public String getOverlap() {
        return overlap;
    }

    public String getClustering() {
        return clustering;
    }

    public String getClusteringValue() {
        return clusteringValue;
    }

    public String getPercentuage() {
        return percentuage;
    }

    public String getThreshold() {
        return threshold;
    }

    public void setFile_not_found(String file_not_found) {
        this.file_not_found = file_not_found;
    }

    public void setCosine(String cosine) {
        this.cosine = cosine;
    }

    public void setSoresen_dice(String soresen_dice) {
        this.soresen_dice = soresen_dice;
    }

    public void setOverlap(String overlap) {
        this.overlap = overlap;
    }

    public void setClustering(String clustering) {
        this.clustering = clustering;
    }

    public void setClusteringValue(String clusteringValue) {
        this.clusteringValue = clusteringValue;
    }

    public void setPercentuage(String percentuage) {
        this.percentuage = percentuage;
    }

    public void setThreshold(String threshold) {
        this.threshold = threshold;
    }
}
