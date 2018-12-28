package com.bankcomm.services;


import com.bankcomm.domain.News;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.List;

public interface NewsService {
    Page<News> getAllNews(Pageable pageable, String type);

    News getNewsById(Integer id);

    Page<News> getAllHotNews(Pageable pageable, String hot);

    List<News> getTopHotNews();

    List<News> getRecommendNewsList(String type);
}
