package com.bankcomm.repositories;

import com.bankcomm.domain.News;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.PagingAndSortingRepository;

import java.util.List;

public interface NewsRepository extends PagingAndSortingRepository<News, Integer> {
//    @Query(nativeQuery = true, name = "getAllHotNews")
//    Page<News> getAllHotNews(Pageable pageable);

    Page<News> findAllByHotEquals(Pageable pageable, String hot);

    @Query(nativeQuery = true, name = "getTopHotNews")
    List<News> getTopHotNews();

    Page<News> findAllByTypeEquals(Pageable pageable, String type);
}
