package com.bankcomm.domain;

import javax.persistence.*;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlRootElement;
import java.io.Serializable;
import java.sql.Blob;
import java.util.Arrays;
import java.util.Base64;
import java.util.Date;

@Entity
@Table(name = "NEWS")
//@SqlResultSetMappings(
//        value = {
//                @SqlResultSetMapping(
//                        name="getAllHotNews",
//                        classes = {
//                                @ConstructorResult(
//                                        targetClass = News.class,
//                                        columns = {
//                                                @ColumnResult(name = "id", type = Integer.class),
//                                                @ColumnResult(name = "url", type = String.class),
//                                                @ColumnResult(name = "title", type = String.class),
//                                                @ColumnResult(name = "content", type = String.class),
//                                                @ColumnResult(name = "cover", type = byte[].class),
//                                                @ColumnResult(name = "type", type = String.class),
//                                                @ColumnResult(name = "keywords", type = String.class),
//                                                @ColumnResult(name = "hot", type = String.class),
//                                                @ColumnResult(name = "update", type = String.class),
//                                                @ColumnResult(name = "batch", type = Date.class)}
//                                )
//                        }
//                ),
//                @SqlResultSetMapping(
//                        name="getTopHotNews",
//                        classes = {
//                                @ConstructorResult(
//                                        targetClass = News.class,
//                                        columns = {
//                                                @ColumnResult(name = "id", type = Integer.class),
//                                                @ColumnResult(name = "url", type = String.class),
//                                                @ColumnResult(name = "title", type = String.class),
//                                                @ColumnResult(name = "content", type = String.class),
//                                                @ColumnResult(name = "cover", type = byte[].class),
//                                                @ColumnResult(name = "type", type = String.class),
//                                                @ColumnResult(name = "keywords", type = String.class),
//                                                @ColumnResult(name = "hot", type = String.class),
//                                                @ColumnResult(name = "update", type = String.class),
//                                                @ColumnResult(name = "batch", type = Date.class)}
//                                )
//                        }
//                )
//        }
//)
@SqlResultSetMappings(
        value = {
                @SqlResultSetMapping(
                        name="getAllHotNews",
                        entities=@EntityResult(
                                entityClass=News.class,
                                fields={
                                        @FieldResult(name="id", column="id"),
                                        @FieldResult(name="url", column="url"),
                                        @FieldResult(name="title", column="title"),
                                        @FieldResult(name="content", column="content"),
                                        @FieldResult(name="cover", column="cover"),
                                        @FieldResult(name="type", column="type"),
                                        @FieldResult(name="keywords", column="keywords"),
                                        @FieldResult(name="hot", column="hot"),
                                        @FieldResult(name="update", column="update"),
                                        @FieldResult(name="batch", column="batch")
                                }
                        )
                ),
                @SqlResultSetMapping(
                        name="getTopHotNews",
                        entities=@EntityResult(
                                entityClass=News.class,
                                fields={
                                        @FieldResult(name="id", column="id"),
                                        @FieldResult(name="url", column="url"),
                                        @FieldResult(name="title", column="title"),
                                        @FieldResult(name="content", column="content"),
                                        @FieldResult(name="cover", column="cover"),
                                        @FieldResult(name="type", column="type"),
                                        @FieldResult(name="keywords", column="keywords"),
                                        @FieldResult(name="hot", column="hot"),
                                        @FieldResult(name="update", column="update"),
                                        @FieldResult(name="batch", column="batch")
                                }
                        )
                )
        }
)
@NamedNativeQueries(
        value = {
                @NamedNativeQuery(
                        name="getAllHotNews",
                        query = "SELECT * FROM {h-schema}NEWS WHERE HOT = '1'",
                        resultClass = News.class,
                        resultSetMapping = "getAllHotNews"
                ),
                @NamedNativeQuery(
                        name="getTopHotNews",
                        query = "SELECT * FROM {h-schema}NEWS WHERE HOT = '1' FETCH FIRST 20 ROWS ONLY",
                        resultClass = News.class,
                        resultSetMapping = "getTopHotNews"
                ),
        }
)
@XmlRootElement
@XmlAccessorType(XmlAccessType.FIELD)
public class News  implements Serializable {
    @Id
    @Column()
    private Integer id;
    @Column()
    private String url;
    @Column()
    private String title;
    @Column()
    private String content;
    @Lob @Basic(fetch = FetchType.LAZY)
    @Column(name = "cover", columnDefinition="BLOB")
    private byte[] cover;
    @Column()
    private String type;
    @Column()
    private String keywords;
    @Column()
    private String hot;
    @Column()
    private String update;
    @Column()
    private Date batch;

    public News() {
    }

    public News(Integer id, String url, String title, String content, byte[] cover, String type, String keywords, String hot, String update, Date batch) {
        this.id = id;
        this.url = url;
        this.title = title;
        this.content = content;
        this.cover = cover;
        this.type = type;
        this.keywords = keywords;
        this.hot = hot;
        this.update = update;
        this.batch = batch;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public byte[] getCover() {
        return cover;
    }

    public void setCover(byte[] cover) {
        this.cover = cover;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getKeywords() {
        return keywords;
    }

    public void setKeywords(String keywords) {
        this.keywords = keywords;
    }

    public String getHot() {
        return hot;
    }

    public void setHot(String hot) {
        this.hot = hot;
    }

    public String getUpdate() {
        return update;
    }

    public void setUpdate(String update) {
        this.update = update;
    }

    public Date getBatch() {
        return batch;
    }

    public void setBatch(Date batch) {
        this.batch = batch;
    }

    @Override
    public String toString() {
        return "News{" +
                "id=" + id +
                ", url='" + url + '\'' +
                ", title='" + title + '\'' +
                ", content='" + content + '\'' +
                ", cover=" + Arrays.toString(cover) +
                ", type='" + type + '\'' +
                ", keywords='" + keywords + '\'' +
                ", hot='" + hot + '\'' +
                ", update='" + update + '\'' +
                ", batch=" + batch +
                '}';
    }
}
