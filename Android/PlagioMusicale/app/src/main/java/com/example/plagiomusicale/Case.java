package com.example.plagiomusicale;

import android.graphics.drawable.Drawable;

import java.io.Serializable;

public class Case implements Serializable {
    private String id,title,first_song,second_song,date_posted,pathFile,info,user_id;
    private DataResult dataResult;
    private boolean is_plagiarism, has_trial,has_verdict;
    public Case() {
    }

    public Case(String title, String first_song, String second_song, String date_posted) {
        this.title = title;
        this.first_song = first_song;
        this.second_song = second_song;
        this.date_posted = date_posted;
    }

    public Case(String id, String title, String first_song, String second_song, String date_posted, boolean has_trial, boolean has_verdict, String pathFile, String info, String user_id, DataResult dataResult, boolean is_plagiarism) {
        this.id = id;
        this.title = title;
        this.first_song = first_song;
        this.second_song = second_song;
        this.date_posted = date_posted;
        this.has_trial = has_trial;
        this.has_verdict = has_verdict;
        this.pathFile = pathFile;
        this.info = info;
        this.user_id = user_id;
        this.dataResult = dataResult;
        this.is_plagiarism= is_plagiarism;
    }

    public void setId(String id) {
        this.id = id;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public boolean getIs_plagiarism() {
        return is_plagiarism;
    }

    public void setPlagiarism(boolean plagiarism) {
        is_plagiarism = plagiarism;
    }

    public void setFirst_song(String first_song) {
        this.first_song = first_song;
    }

    public void setSecond_song(String second_song) {
        this.second_song = second_song;
    }

    public void setDate_posted(String date_posted) {
        this.date_posted = date_posted;
    }

    public void setHas_trial(boolean has_trial) {
        this.has_trial = has_trial;
    }

    public void setHas_verdict(boolean has_verdict) {
        this.has_verdict = has_verdict;
    }

    public void setPathFile(String pathFile) {
        this.pathFile = pathFile;
    }

    public void setInfo(String info) {
        this.info = info;
    }

    public void setUser_id(String user_id) {
        this.user_id = user_id;
    }

    public void setDataResult(DataResult dataResult) {
        this.dataResult = dataResult;
    }

    public String getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public String getFirst_song() {
        return first_song;
    }

    public String getSecond_song() {
        return second_song;
    }

    public String getDate_posted() {
        return date_posted;
    }

    public boolean getHas_trial() {
        return has_trial;
    }

    public boolean getHas_verdict() {
        return has_verdict;
    }

    public String getPathFile() {
        return pathFile;
    }

    public String getInfo() {
        return info;
    }

    public String getUser_id() {
        return user_id;
    }

    public DataResult getDataResult() {
        return dataResult;
    }
}


