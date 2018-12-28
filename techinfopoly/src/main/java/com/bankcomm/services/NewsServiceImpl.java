package com.bankcomm.services;

import com.bankcomm.domain.News;
import com.bankcomm.repositories.NewsRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class NewsServiceImpl implements NewsService {
    private NewsRepository newsRepository;

    @Autowired
    public void setNewsRepository(NewsRepository newsRepository) {
        this.newsRepository = newsRepository;
    }

    @Override
    public Page<News> getAllNews(Pageable pageable, String type) {
        return newsRepository.getAllByType(pageable, type);
    }

    @Override
    public News getNewsById(Integer id) {
        return newsRepository.findById(id).orElse(null);
    }

    @Override
    public Page<News> getAllHotNews(Pageable pageable, String hot) {
        return newsRepository.getAllByHot(pageable, hot);
    }

    @Override
    public List<News> getTopHotNews() {
        return newsRepository.getTopHotNews();
    }

    @Override
    public List<News> getRecommendNewsList(String type) {
        return newsRepository.getRecommendNewsList(type);
    }
}
